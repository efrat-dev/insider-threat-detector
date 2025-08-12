# Advanced Insider Threat Dataset Generator

A sophisticated command-line tool for generating realistic insider threat datasets for cybersecurity research and analysis.

## 📋 Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Command Line Arguments](#command-line-arguments)
- [Examples](#examples)
- [Output Formats](#output-formats)
- [Technical Details](#technical-details)
- [Code Documentation](#code-documentation)

## 📁 Project Structure

```
cli/
├── argument_parser.py    # Command-line argument parsing and validation
├── display_utils.py      # User interface and display utilities
└── README.md            # This documentation file
```

## 🚀 Installation

```bash
# Clone the repository
git clone <repository-url>
cd advanced-insider-threat-generator

# Install dependencies
pip install -r requirements.txt
```

## 💻 Usage

### Basic Usage

Generate a default dataset:
```bash
python main.py
```

### Advanced Usage

Generate a custom dataset with specific parameters:
```bash
python main.py -e 1000 -d 180 -m 0.12 --add-noise --verbose
```

## 🔧 Command Line Arguments

### Dataset Parameters
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `-e, --employees` | int | 100 | Number of employees to generate |
| `-d, --days` | int | 30 | Number of days to simulate |
| `-m, --malicious-ratio` | float | 0.05 | Ratio of malicious employees (0-1) |

### Output Options
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `-o, --output` | str | insider_threat_advanced | Output filename prefix |
| `--export-format` | choice | both | Export format: csv, excel, or both |
| `--output-dir` | str | ./output | Output directory path |

### Analysis Options
| Argument | Description |
|----------|-------------|
| `--analysis-only` | Run analysis on existing dataset only |
| `--input-file` | Input CSV file for analysis-only mode |
| `--skip-analysis` | Skip statistical analysis generation |
| `--validate-data` | Run comprehensive data validation |

### Technical Options
| Argument | Description |
|----------|-------------|
| `--seed` | Random seed for reproducible results |
| `--verbose` | Enable detailed output logging |
| `--quiet` | Suppress all output except errors |

### Noise Injection Options
| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--add-noise` | flag | False | Enable synthetic noise injection |
| `--burn-noise-rate` | float | 0.05 | Burn activity noise percentage |
| `--print-noise-rate` | float | 0.05 | Print activity noise percentage |
| `--entry-time-noise-rate` | float | 0.10 | Entry time noise percentage |
| `--use-gaussian` | flag | False | Use Gaussian noise distribution |

## 📚 Examples

### Example 1: Small Test Dataset
```bash
python main.py -e 50 -d 7 -m 0.10 --verbose
```
*Generates a 7-day dataset with 50 employees, 10% malicious ratio*

### Example 2: Large Production Dataset
```bash
python main.py -e 5000 -d 365 -m 0.08 --add-noise --seed 42
```
*Generates a full-year dataset with 5,000 employees, noise injection, and reproducible seeding*

### Example 3: Analysis Only
```bash
python main.py --analysis-only --input-file existing_dataset.csv --validate-data
```
*Analyzes an existing dataset with comprehensive validation*

### Example 4: Excel Export Only
```bash
python main.py -e 200 -d 30 --export-format excel --output quarterly_report
```
*Generates a 30-day dataset exported only to Excel format*

## 📊 Output Formats

### CSV Output
- **Filename**: `{prefix}.csv`
- **Features**: Lightweight, universal compatibility
- **Best for**: Data analysis, machine learning pipelines

### Excel Output  
- **Filename**: `{prefix}.xlsx`
- **Features**: Formatted sheets, charts, summary statistics
- **Best for**: Business reporting, presentation-ready analysis

### Combined Output
- Both CSV and Excel files generated simultaneously
- Consistent data across formats with format-specific optimizations

## 🔍 Technical Details

### Validation System
The tool implements comprehensive argument validation including:
- Range checks for numerical parameters (employees: 1-10,000, days: 1-1,000)
- Ratio validation for malicious employee percentage (0.0-1.0)
- File existence verification for analysis-only mode
- Logical conflict detection (e.g., verbose + quiet flags)

### Noise Injection Algorithm
Advanced noise injection system featuring:
- **Burn Noise**: Simulates data destruction activities
- **Print Noise**: Adds realistic printing behavior variations  
- **Entry Time Noise**: Introduces temporal anomalies
- **Gaussian Distribution**: Optional statistical noise modeling

### Error Handling
Robust error handling with:
- Pre-execution argument validation
- Graceful failure modes with descriptive error messages
- Comprehensive logging for debugging and auditing

## 📖 Code Documentation

### Core Modules

#### [`argument_parser.py`](cli/argument_parser.py)
Handles command-line interface functionality:
- **`parse_arguments()`**: Configures and parses CLI arguments using argparse
- **`validate_arguments()`**: Performs comprehensive argument validation
- Organized argument groups for better UX
- Extensive help text and usage examples

#### [`display_utils.py`](cli/display_utils.py)  
Manages user interface and output display:
- **`print_configuration()`**: Displays current generation settings
- **`print_final_statistics()`**: Shows dataset statistics and distributions
- **`print_success_message()`**: Confirmation and file listing
- Consistent formatting and professional output styling

### Key Design Patterns
- **Separation of Concerns**: Clean separation between parsing, validation, and display logic
- **Comprehensive Documentation**: Detailed docstrings for all functions and parameters
- **User Experience Focus**: Clear error messages, helpful examples, and intuitive argument organization
- **Extensibility**: Modular design allows for easy feature additions and modifications
