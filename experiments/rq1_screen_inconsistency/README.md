# RQ1: Screen Inconsistency Detection

This experiment evaluates the screen inconsistency detection capabilities of GUIPilot by comparing different matchers and checkers on mutated screens.

## Overview

This experiment tests the ability of GUIPilot to detect inconsistencies between two screens (original and mutated). It evaluates:

- **Widget Matching**: How well different matchers can pair widgets across screens
- **Inconsistency Detection**: How accurately checkers can identify differences (bounding box, color, text)

## Research Question

**RQ1**: How effective is GUIPilot at detecting screen inconsistencies compared to baseline methods?

## Environment Setup

### Prerequisites

1. **Conda Environment**: Ensure the `guipilot` conda environment is activated
   ```bash
   conda activate guipilot
   ```

2. **GUIPilot Package**: Make sure GUIPilot is installed
   ```bash
   cd /path/to/GUIPilot-main
   pip install .
   ```

3. **Environment Variables**: Set the dataset path
   ```bash
   export DATASET_PATH=/path/to/your/dataset
   ```

   Or create a `.env` file in this directory:
   ```
   DATASET_PATH=/path/to/your/dataset
   ```

### Optional: OCR Service

If you want to use automatic widget detection (instead of pre-annotated JSON files), you need to run an OCR service on `localhost:5000`. However, this is **not required** if your dataset already contains widget annotations in JSON format.

## Dataset Structure

The dataset should be organized as follows:

```
dataset/
├── App1/
│   ├── 1.jpg          # Screenshot image
│   ├── 1.json         # Widget annotations (LabelMe format)
│   ├── 2.jpg
│   ├── 2.json
│   └── ...
├── App2/
│   ├── 1.jpg
│   ├── 1.json
│   └── ...
└── ...
```

### JSON Annotation Format

Each JSON file should follow the LabelMe format:

```json
{
  "version": "4.5.6",
  "flags": {},
  "shapes": [
    {
      "label": "Button",
      "points": [[x1, y1], [x2, y2]],
      "group_id": null,
      "shape_type": "rectangle",
      "flags": {}
    },
    ...
  ],
  "imagePath": "1.jpg",
  "imageData": "..."
}
```

Supported widget types (labels) include:
- `Button`
- `Text`
- `Image`
- `Input`
- `CheckBox`
- `RadioButton`
- `Switch`
- `Slider`
- `ProgressBar`
- And other standard mobile UI components

## Running the Experiment

### Basic Usage

```bash
cd /path/to/GUIPilot-main/experiments/rq1_screen_inconsistency
export DATASET_PATH=/path/to/your/dataset
python main.py
```

### Experiment Process

The experiment performs the following steps for each image in the dataset:

1. **Load Screen**: Load the original screen with its widget annotations
2. **Apply Mutation**: Create a mutated version of the screen with one of the following mutations:
   - `insert_row`: Insert a new row of widgets
   - `delete_row`: Delete a row of widgets
   - `swap_widgets`: Swap positions of two widgets
   - `change_widgets_text`: Change the text content of widgets
   - `change_widgets_color`: Change the color of widgets
3. **Match Widgets**: Use matchers to pair widgets between original and mutated screens
4. **Check Inconsistencies**: Use checkers to identify inconsistencies
5. **Calculate Metrics**: Compute precision, recall, and other evaluation metrics
6. **Visualize Results**: Generate visualization images showing detected inconsistencies

### Mutation Types

The experiment tests 5 types of mutations:

1. **insert_row**: Inserts a new row of widgets (5% mutation rate)
2. **delete_row**: Deletes a row of widgets (5% mutation rate)
3. **swap_widgets**: Swaps positions of two widgets (5% mutation rate)
4. **change_widgets_text**: Changes text content of widgets (5% mutation rate)
5. **change_widgets_color**: Changes color of widgets (5% mutation rate)

### Matchers and Checkers

The experiment compares:

- **Matchers**:
  - `gvt`: GVT (Graph-based Visual Tracking) matcher
  - `guipilot`: GUIPilot V2 matcher

- **Checker**:
  - `gvt`: GVT checker (detects bounding box, color, and text inconsistencies)

## Output Files

### 1. Evaluation Results (`evaluation.csv`)

Contains detailed metrics for each test case:

| Column | Description |
|--------|-------------|
| `id` | Path to the test image |
| `mutation` | Type of mutation applied |
| `matcher` | Matcher used (gvt or guipilot) |
| `checker` | Checker used (gvt) |
| `cls_tp` | Number of correctly identified inconsistencies (correct pair & type) |
| `tp` | Number of correctly identified inconsistencies (correct pair) |
| `fp` | Number of false positives |
| `fn` | Number of false negatives |
| `match_time` | Time taken for widget matching (seconds) |
| `check_time` | Time taken for inconsistency checking (seconds) |

### 2. Visualization Results (`visualize/`)

Directory structure:
```
visualize/
├── gvt_gvt/
│   ├── delete_row/
│   │   ├── App1/
│   │   │   ├── 1.jpg      # Visualization image
│   │   │   └── 1.txt      # Detailed results
│   │   └── ...
│   ├── swap_widgets/
│   ├── change_widgets_text/
│   └── change_widgets_color/
└── guipilot_gvt/
    └── (same structure)
```

Each visualization includes:
- **Image (`.jpg`)**: Side-by-side comparison showing:
  - Green boxes: Correctly matched widgets
  - Yellow boxes: Matched widgets with inconsistencies
  - Red boxes: Unmatched widgets or incorrectly matched widgets
- **Text (`.txt`)**: Detailed information including:
  - Matched widget pairs
  - Detected inconsistencies (predicted and ground truth)
  - Edit distance representation

## Understanding the Results

### Metrics Explanation

- **cls_tp** (Class True Positive): Number of inconsistencies correctly identified with both correct widget pair and correct inconsistency type
- **tp** (True Positive): Number of inconsistencies correctly identified (correct widget pair, regardless of type)
- **fp** (False Positive): Number of inconsistencies incorrectly reported
- **fn** (False Negative): Number of inconsistencies that were not detected

### Performance Metrics

From the metrics, you can calculate:

- **Precision** = tp / (tp + fp)
- **Recall** = tp / (tp + fn)
- **Class Precision** = cls_tp / tp
- **F1-Score** = 2 × (Precision × Recall) / (Precision + Recall)

### Example Analysis

After running the experiment, you can analyze results:

```python
import pandas as pd

df = pd.read_csv('evaluation.csv')

# Overall performance by matcher
for matcher in df['matcher'].unique():
    subset = df[df['matcher'] == matcher]
    tp = subset['tp'].sum()
    fp = subset['fp'].sum()
    fn = subset['fn'].sum()

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    print(f"{matcher}: Precision={precision:.2f}, Recall={recall:.2f}, F1={f1:.2f}")
```

## Troubleshooting

### Issue: No images found

**Error**: `Found 0 images`

**Solution**:
- Check that `DATASET_PATH` is set correctly
- Ensure image files are named with numeric names (e.g., `1.jpg`, `2.jpg`)
- Verify the directory structure matches the expected format

### Issue: OCR service connection error

**Error**: `HTTPConnectionPool(host='localhost', port=5000): Max retries exceeded`

**Solution**:
- This is **not an error** if you're using pre-annotated JSON files
- The experiment will use the JSON annotations instead of OCR
- If you need OCR, start the OCR service on `localhost:5000`

### Issue: Module import errors

**Error**: `ModuleNotFoundError: No module named 'guipilot.models.detector'`

**Solution**:
- Ensure GUIPilot is properly installed: `pip install .`
- Check that all `__init__.py` files exist in the `guipilot/models/` subdirectories
- Reinstall if necessary: `pip install . --force-reinstall`

### Issue: JSON parsing errors

**Error**: Errors when loading JSON annotation files

**Solution**:
- Verify JSON files follow the LabelMe format
- Check that each shape has `points` and `label` fields
- Ensure coordinates are valid (x1 < x2, y1 < y2)

## Expected Runtime

The experiment runtime depends on:
- Number of images in the dataset
- Number of mutation types (5)
- Number of matchers (2)
- Image resolution and number of widgets

**Approximate time per test case**:
- Widget matching: 0.5-10 seconds (depending on matcher)
- Inconsistency checking: 100-300 seconds (depending on screen complexity)

For a dataset with 4 images, expect approximately **1-2 hours** of runtime.

## Citation

If you use this experiment in your research, please cite:

```bibtex
@article{liu2025guipilot,
  title={GUIPilot: A Consistency-Based Mobile GUI Testing Approach for Detecting Application-Specific Bugs},
  author={Liu, Ruofan and Teoh, Xiwen and Lin, Yun and Chen, Guanjie and Ren, Ruofei and Poshyvanyk, Denys and Dong, Jin Song},
  journal={Proceedings of the ACM on Software Engineering},
  volume={2},
  number={ISSTA},
  pages={753--776},
  year={2025},
  publisher={ACM New York, NY, USA}
}
```

## Additional Resources

- [GUIPilot Project Page](https://sites.google.com/view/guipilot/home)
- [Dataset Repository](https://zenodo.org/records/15107436)
- [Model Repository](https://huggingface.co/code-philia/GUIPilot)
- [Paper](http://linyun.info/publications/issta25.pdf)

## Contact

For questions or issues, please refer to the main GUIPilot repository or open an issue on GitHub.
