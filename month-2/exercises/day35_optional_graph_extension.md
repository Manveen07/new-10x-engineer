# Day 35: Optional Graph Extension

## Goal

Treat graph retrieval as a measured experiment, not the core Month 2 path.

## Build Only If Baseline Is Stable

- extract entities from chunks.
- store `entities` and `entity_mentions`, or use Neo4j as an experiment.
- boost chunks connected to query entities.
- compare against hybrid baseline.

## Done When

- Graph extension can be enabled/disabled with config.
- Benchmark shows whether it helped.
