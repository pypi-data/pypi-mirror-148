use std::env;

use actix_cors::Cors;
use actix_files as fs;
use actix_web::{App, HttpRequest, HttpResponse, HttpServer, post, Responder};
use actix_web::http::header::HeaderMap;
use pyo3::prelude::*;

use reuse::touch;
use reuse::write_file;

mod reuse;

#[post("/api/log_msgpack/")]
async fn log_msgpack(req: HttpRequest, body: String) -> impl Responder {
    let map_header = req.headers();
    let mut result: String = "{".to_string();
    result.push_str(r#""headers":""#);
    for key in map_header.keys() {
        reuse::append_str(&mut result, map_header, key.as_str());
    }
    result.push_str(r#"","body":"#);
    result.push_str(&body);
    result.push_str(r#"}"#);
    let bytes = reuse::json_to_bytes(&result);
    let path = "output.msgpack";
    touch(path);
    write_file(path, &bytes);
    HttpResponse::Ok().body(path)
}

#[post("/api/echo/")]
async fn echo(body: String) -> impl Responder {
    HttpResponse::Ok().body(body)
}

#[actix_rt::main]
#[pyfunction]
async fn actix_server(host: &str, int_port: usize) -> std::io::Result<()> {
    print_current_directory();
    print_user_test();
    let http_server = HttpServer::new(|| {
        App::new()
            .wrap(
                Cors::default()
                    .send_wildcard()
                    .allow_any_method()
                    .allow_any_header()
                    .allow_any_origin()
                    .max_age(3600),
            )
            .service(log_msgpack)
            .service(echo)
            .service(fs::Files::new("/data/", "data/").show_files_listing())
    });
    http_server.bind(host_port(host, int_port))?.run().await
}

fn host_port(host: &str, int_port: usize) -> String {
    let str_ip_port = format!("{}:{}", host, int_port);
    println!("cameo_ocean actix server at {}", str_ip_port);
    str_ip_port
}

fn print_current_directory() {
    let path = env::current_dir().unwrap();
    println!("The current directory is {}", path.display());
}

fn print_user_test() {
    println!(
        "
== local test ==
sh/curl.sh
"
    );
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a + b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn cameo_ocean(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(actix_server, m)?)?;
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    Ok(())
}
