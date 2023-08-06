use pyo3::prelude::*;
use chrono::{DateTime, Local, TimeZone, FixedOffset};
use lazy_static::lazy_static;
use regex::Regex;

/// A Python module implemented in Rust.
#[pymodule]
fn evg_task_profiler_py(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<State>()?;
    m.add_class::<TimingInfo>()?;
    Ok(())
}

struct Event {
    name: String,
    step: String,
}

#[pyclass]
#[derive(Clone)]
pub struct TimingInfo {
    #[pyo3(get)]
    pub name: String,
    #[pyo3(get)]
    pub step: String,
    #[pyo3(get)]
    pub index: usize,
    #[pyo3(get)]
    pub duration: i64,
}

fn parse_timestamp(line: &str) -> Option<DateTime<Local>> {
    lazy_static! {
        static ref TIMESTAMP_RE: Regex =
            Regex::new(r#"^\[(\d{4})/(\d{2})/(\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3})\] "#).unwrap();
    }
    TIMESTAMP_RE.captures(line).map(|caps| {
        Local
            .ymd(
                caps[1].parse().unwrap(),
                caps[2].parse().unwrap(),
                caps[3].parse().unwrap(),
            )
            .and_hms_milli(
                caps[4].parse().unwrap(),
                caps[5].parse().unwrap(),
                caps[6].parse().unwrap(),
                caps[7].parse().unwrap(),
            )
    })
}

fn parse_start_event(line: &str) -> Option<Event> {
    lazy_static! {
        static ref START_RE: Regex =
            Regex::new(r#"^\[.*] Running command (.*) \((step .*)\)$"#).unwrap();
    }
    START_RE.captures(line).map(|caps| Event {
        name: caps[1].to_string(),
        step: caps[2].to_string(),
    })
}

fn parse_end_event(line: &str) -> Option<Event> {
    lazy_static! {
        static ref FINISHED_RE: Regex =
            Regex::new(r#"^\[.*] Finished '(.*)' in "(.*)" in (.*)$"#).unwrap();
    }
    FINISHED_RE.captures(line).map(|caps| Event {
        name: caps[1].to_string(),
        step: caps[2].to_string(),
    })
}

enum ParserState {
    Start,
    InStep {
        name: String,
        step: String,
        start_time: DateTime<FixedOffset>,
    },
}

#[pyclass]
struct State {
    parser_state: ParserState,
    pub events: Vec<TimingInfo>,
    index: usize,
    total_time: i64,
}

#[pymethods]
impl State {
    #[new]
    pub fn new() -> Self {
        Self {
            parser_state: ParserState::Start,
            events: vec![],
            index: 0,
            total_time: 0,
        }
    }

    pub fn process_line(&mut self, line: &str) {
        if let Some(dt) = parse_timestamp(line) {
            if let Some(event) = parse_start_event(line) {
                self.start_event(&event.name, &event.step, &dt.to_rfc3339());
            } else if let Some(_caps) = parse_end_event(line) {
                self.end_event(&dt.to_rfc3339());
            }
        }
    }

    pub fn get_events(&self) -> Vec<TimingInfo> {
        self.events.clone()
    }

    fn start_event(&mut self, name: &str, step: &str, dt: &str) {
        let dt = DateTime::parse_from_rfc3339(dt).unwrap();
        if let ParserState::InStep {
            name,
            step,
            start_time,
        } = &self.parser_state
        {
            let duration = dt - *start_time;
            self.events.push(TimingInfo {
                name: name.to_string(),
                step: step.to_string(),
                index: self.index,
                duration: duration.num_milliseconds(),
            });
            self.index += 1;
            self.total_time += duration.num_milliseconds();
        }
        self.parser_state = ParserState::InStep {
            name: name.to_string(),
            step: step.to_string(),
            start_time: dt,
        };
    }

    fn end_event(&mut self, dt: &str) {
        let dt = DateTime::parse_from_rfc3339(dt).unwrap();
        if let ParserState::InStep {
            name,
            step,
            start_time,
        } = &self.parser_state
        {
            let duration = dt - *start_time;
            self.events.push(TimingInfo {
                name: name.to_string(),
                step: step.to_string(),
                index: self.index,
                duration: duration.num_milliseconds(),
            });
            self.index += 1;
            self.total_time += duration.num_milliseconds();
            self.parser_state = ParserState::Start;
        }
    }
}
