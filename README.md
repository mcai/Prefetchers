# Cache Prefetcher Simulation

This project simulates two types of cache prefetchers: Markov Prefetcher and Stride Prefetcher. The prefetchers are tested against different memory access patterns, and their accuracy is calculated.

## Files

- markov_predictor.py: Contains the implementation of the Markov Prefetcher and its simulation.
- stride_prefetcher.py: Contains the implementation of the Stride Prefetcher and its simulation.
- access_patterns.py: Contains functions to generate different memory access patterns and a function to generate a Markdown table for the results.

## Usage

1. Run markov_predictor.py to simulate the Markov Prefetcher with different memory access patterns. The output will display the accuracy of the prefetcher for each pattern and a Markdown table with the results.

```bash
python markov_predictor.py
```

2. Run stride_prefetcher.py to simulate the Stride Prefetcher with different memory access patterns. The output will display the accuracy of the prefetcher for each pattern and a Markdown table with the results.

```bash
python stride_prefetcher.py
```

## Example Output

The output will be in the following format:

```bash
Sequential access pattern:
...
Accuracy: 0.9
...
Strided access pattern:
...
Accuracy: 0.8
...
Interleaved access pattern:
...
Accuracy: 0.7
...
Random access pattern:
...
Accuracy: 0.6
...

Results in Markdown table:
| Access Pattern | Accuracy |
| -------------- | -------- |
| Sequential     | 0.9      |
| Strided        | 0.8      |
| Interleaved    | 0.7      |
| Random         | 0.6      |
```