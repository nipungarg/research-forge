# Research Forge — Autonomous Research Assistant

## Overview

Research Forge is a controlled single-agent system that performs structured research by iteratively gathering evidence, synthesizing insights, and citing sources.

## Why Not a Pipeline?

Traditional pipelines fail because research is not linear:

* Information may be incomplete
* Additional search may be required
* Quality must be evaluated dynamically

This system uses an agent loop to make decisions at runtime.

## Core Idea

The agent operates using:

* A decision loop (Observe → Think → Act)
* Explicit memory
* Controlled tools

## Goal

Given a research question, produce:

* Structured summary
* Supporting evidence
* Source attribution
