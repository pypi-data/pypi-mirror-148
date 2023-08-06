use std::fs::OpenOptions;
use std::io::Write;
use std::path::Path;
use serde_json::Value;
use crate::HeaderMap;

pub fn touch(path: &str) {
    OpenOptions::new().create(true).write(true).open(Path::new(path)).unwrap();
}

pub fn write_file(path: &str, bytes: &Vec<u8>) {
    let mut file = OpenOptions::new()
        .write(true)
        .append(true)
        .open(path)
        .unwrap();
    file.write_all(bytes).unwrap();
}

pub fn append_str(result: &mut String, map: &HeaderMap, key: &str) {
    result.push_str(format!("{}: {}\\n", key, map.get(key).unwrap().to_str().unwrap()).as_str());
}

pub fn json_to_bytes(result: &String) -> Vec<u8> {
    let v: Value = serde_json::from_str(&result).unwrap();
    let bytes = rmp_serde::to_vec(&v).unwrap();
    bytes
}
