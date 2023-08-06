use crate::export::export_bed;

use pyo3::{
    prelude::*,
    PyResult, Python,
    type_object::PyTypeObject,
    exceptions::PyTypeError,
};
use std::process::Command;
use tempfile::Builder;
use std::path::Path;
use polars::prelude::{DataFrame, CsvReader};
use polars::prelude::SerReader;
use anndata_rs::anndata_trait::{Mapping, DataIO};
use snapatac2_core::utils::get_reference_seq_info;
use pyanndata::{AnnData, AnnDataSet};
use std::collections::{HashSet, HashMap};
use rayon::iter::{IntoParallelIterator, ParallelIterator};

#[pyfunction]
pub fn call_peaks<'py>(
    py: Python<'py>,
    data: &PyAny,
    group_by: Vec<&str>,
    selections: Option<HashSet<&str>>,
    q_value: f64,
    key_added: &str,
) -> PyResult<()> {
    let dir = Builder::new().tempdir_in("./").unwrap();

    eprintln!("preparing input...");
    let files = export_bed(
        py, data, group_by.clone(), group_by, selections,
        dir.path().to_str().unwrap(), "", ".bed.gz",
    )?;

    let ref_genome = if data.is_instance(AnnData::type_object(py))? {
        let anndata: AnnData = data.extract()?;
        let x = get_reference_seq_info(&mut anndata.0.inner().get_uns().inner()).unwrap();
        x
    } else if data.is_instance(AnnDataSet::type_object(py))? {
        let anndata: AnnDataSet = data.extract()?;
        let x = get_reference_seq_info(
            &mut anndata.0.inner().anndatas.inner().iter().next().unwrap()
                .1.get_uns().inner()
        ).unwrap();
        x
    } else {
        return Err(PyTypeError::new_err("expecting an AnnData or AnnDataSet object"));
    };
    let genome_size = ref_genome.iter().map(|(_, v)| *v).sum();

    eprintln!("calling peaks for {} groups...", files.len());
    let m: HashMap<String, Box<dyn DataIO>> = files.into_par_iter().map(|(k, x)| {
        let df: Box<dyn DataIO> = Box::new(macs2(x, q_value, genome_size, dir.path()));
        eprintln!("group {}: done!", k);
        (k, df)
    }).collect();
    let mapping: Box<dyn DataIO> = Box::new(Mapping(m));

    if data.is_instance(AnnData::type_object(py))? {
        let anndata: AnnData = data.extract()?;
        anndata.0.inner().get_uns().inner().add_data(key_added, &mapping).unwrap();
    } else if data.is_instance(AnnDataSet::type_object(py))? {
        let anndata: AnnDataSet = data.extract()?;
        anndata.0.inner().get_uns().inner().add_data(key_added, &mapping).unwrap();
    } else {
        return Err(PyTypeError::new_err("expecting an AnnData or AnnDataSet object"));
    }

    dir.close().unwrap();
    Ok(())
}

fn macs2<P1, P2>(
    bed_file: P1,
    q_value: f64,
    genome_size: u64,
    tmp_dir: P2,
) -> DataFrame
where
    P1: AsRef<Path>,
    P2: AsRef<Path>,
{
    let dir = Builder::new().tempdir_in(tmp_dir).unwrap();

    Command::new("macs2").args([
        "callpeak",
        "-f", "BED",
        "-t", bed_file.as_ref().to_str().unwrap(),
        "--keep-dup", "all",
        "--outdir", format!("{}", dir.path().display()).as_str(),
        "--qvalue", format!("{}", q_value).as_str(),
        "-g", format!("{}", (genome_size as f64 * 0.9).round()).as_str(),
        "--call-summits",
        "--nomodel", "--shift", "-100", "--extsize", "200",
        "--nolambda",
        "--tempdir", format!("{}", dir.path().display()).as_str(),
    ]).output().unwrap();

    let file_path = dir.path().join("NA_peaks.narrowPeak");
    let column_names = [
        "chrom", "chromStart", "chromEnd", "name", "score", "strand",
        "signalValue", "pValue", "qValue", "peak"
    ];
    let mut df = CsvReader::from_path(file_path).unwrap()
        .has_header(false)
        .with_delimiter('\t' as u8)
        .finish().unwrap();
    df.set_column_names(&column_names).unwrap();
    dir.close().unwrap();
    df
}
 