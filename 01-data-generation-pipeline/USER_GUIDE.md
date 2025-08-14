# User Guide & Quick Reference

> Everything you need to know to use the Advanced Insider Threat Dataset Generator effectively

📖 **Navigation**: [← Technical Overview](TECHNICAL_OVERVIEW.md) | [Main README](README.md) | [Dataset Schema](DATA_SCHEMA.md)
---

## 🎯 What This Tool Does

This generator creates **classified environment employee datasets** specifically for insider threat research in secure organizations. Unlike standard HR data, it focuses on **security clearance levels, classified document handling, and security protocol compliance** - essential elements for understanding insider threats in government, defense, and high-security environments.

### 🔐 **Unique Security Features**
- **Multi-Level Security Clearances** (Levels 1-4) assigned to employees
- **Classified Document Operations** with classification level tracking
- **Security Protocol Modeling** including clearance-based access restrictions
- **Cross-Classification Risk Detection** identifying potential security violations

## ⚡ Quick Start Commands

### Generate Your First Dataset
```bash
# Small test dataset (50 employees, 7 days)
python main.py --employees 50 --days 7 --verbose

# Standard research dataset (1000 employees, 6 months)
python main.py --employees 1000 --days 180 --malicious-ratio 0.05

# Large production dataset with noise
python main.py --employees 5000 --days 365 --add-noise --seed 42
```

### Analyze Existing Data
```bash
# Analyze your own CSV file
python main.py --analysis-only --input-file your_data.csv

# Validate data quality
python main.py --analysis-only --input-file data.csv --validate-data
```

## 📊 Understanding the Output

### Generated Files
- **`insider_threat_advanced_TIMESTAMP.csv`** - Clean dataset ready for analysis
- **`insider_threat_advanced_TIMESTAMP.xlsx`** - Excel workbook with multiple analysis sheets
- **`analysis_report_TIMESTAMP.txt`** - Comprehensive text report with insights
- **`data_dictionary_TIMESTAMP.txt`** - Complete documentation of all data fields

### Key Data Fields
- **Employee Info**: ID, department, **security clearance level**, behavioral group
- **Daily Activities**: Building access, printing volume, **classified document burning**, travel status
- **Security Metrics**: **Classification levels handled**, clearance violations, unauthorized access attempts
- **Risk Indicators**: Off-hours classified activity, **cross-classification operations**, hostile country travel

### 🔐 **Classification-Specific Fields**
- **`employee_classification`** - Employee security clearance level (1-4)
- **`avg_request_classification`** - Average classification of documents handled
- **`max_request_classification`** - Highest classification level accessed
- **`classification_violation_flag`** - Indicates potential clearance violations
- **`cross_classification_activity`** - Activities spanning multiple classification levels

## 🎛️ Configuration Options

### Dataset Size
```bash
--employees 1000    # Number of employees (1-10,000)
--days 180          # Simulation period (1-1,000 days)
--malicious-ratio 0.05  # Percentage of malicious employees (0.0-1.0)
```

### Output Control
```bash
--output my_dataset         # Custom filename prefix
--export-format excel       # csv, excel, or both
--output-dir ./results      # Custom output directory
```

### Advanced Features
```bash
--add-noise                 # Add synthetic noise for realism
--seed 42                   # Reproducible results
--verbose                   # Detailed logging
--skip-analysis            # Generate data only, skip analysis
```

## 🔄 Typical Workflow

### For Research Projects
1. **Generate Base Dataset** with your required parameters
2. **Review Analysis Reports** to understand behavioral patterns
3. **Export to your preferred format** (CSV for ML, Excel for presentations)
4. **Use data dictionary** to understand all fields and their meanings

### For Classified Environment Research
1. **Configure security clearance distributions** in the configuration files
2. **Generate dataset with realistic classification patterns** 
3. **Analyze clearance-based behavioral differences** using security analysis features
4. **Export classified-aware reports** focusing on security protocol compliance

### For Security Clearance Studies
1. **Set appropriate classification levels** for your organization (1-4 scale)
2. **Model cross-classification activities** to detect potential violations
3. **Use hostile country travel features** for comprehensive risk assessment
4. **Leverage classification violation detection** in the analysis outputs

### For System Development
1. **Start with small datasets** for initial testing (50-100 employees)
2. **Scale up gradually** as your system handles larger volumes
3. **Use reproducible seeds** for consistent testing environments
4. **Leverage analysis-only mode** to test analysis components separately

## 🎯 Behavioral Groups Explained

The system models **6 distinct employee types**:

- **Group A**: Executives - Irregular hours, high travel, moderate document activity
- **Group B**: Engineers - Technical focus, some late hours, low travel
- **Group C**: Office Staff - Regular 9-5, high printing, minimal travel  
- **Group D**: Marketing - Standard hours, moderate travel, regular printing
- **Group E**: Security - 24/7 access, high security clearance, specialized patterns
- **Group F**: IT Staff - Irregular technical hours, high data handling, system access

## 🔍 Analysis Features

### What the Analysis Tells You
- **Behavioral Patterns** by employee group and department
- **Security Risks** including travel to hostile countries and off-hours activity
- **Data Quality** with validation and consistency checks
- **Statistical Insights** including trends and anomaly detection

### Reading the Reports
- **Excel Workbook** contains multiple sheets with different views of your data
- **Text Reports** provide narrative insights and key findings
- **Data Dictionary** explains every field and its possible values
- **Summary Statistics** give you dataset overview and quality metrics

## 🛠️ Customization

### Modify Behavioral Patterns
See [`config/README.md`](config/README.md) for detailed customization guide covering:
- Employee behavioral group patterns
- Organizational structure and departments
- Geographic locations and travel destinations
- Security classification levels

### Add New Activity Types
See [`activity_generators/README.md`](activity_generators/README.md) for extending the system with new activity generators.

## 📚 Detailed Documentation

### Core Functionality
- **[CLI Reference](cli/README.md)** - Complete command-line guide with examples
- **[Configuration System](config/README.md)** - Behavioral patterns and organizational setup
- **[Activity Generation](activity_generators/README.md)** - How employee activities are simulated
- **[Analysis Suite](analyzers/README.md)** - Understanding analysis outputs and metrics

### Technical Details  
- **[Core Infrastructure](core/README.md)** - Workflow management and system utilities
- **[Employee Generation](employee_generator/README.md)** - Employee profile creation process
- **[Data Export](data_exporter/README.md)** - Export formats and documentation generation
- **[Utils and Constants](utils/README.md)** - System constants and utility functions

## 🆘 Common Issues & Solutions

### Large Dataset Performance
- Use batch processing for 5000+ employees
- Enable `--quiet` mode to reduce output overhead
- Consider splitting very large datasets into multiple runs

### Memory Usage
- Monitor memory usage with datasets over 2000 employees
- Use appropriate `--seed` values for reproducible results
- Close other applications when generating large datasets

### Analysis Errors
- Ensure input CSV files have required columns for analysis-only mode
- Check data dictionary for required field formats
- Validate data quality before running analysis

---

## 📚 Complete Documentation Suite

### 📖 **Main Documentation**
- **[🏠 Main Project README](README.md)** - Project overview and introduction
- **[🏗️ Technical Architecture Overview](TECHNICAL_OVERVIEW.md)** - System design and data flow

### 🔧 **Module-Specific Guides**
- **[CLI Complete Reference](cli/README.md)** - All command-line options and advanced examples
- **[Configuration Deep Dive](config/README.md)** - Customizing behavioral patterns and organizational structure
- **[Activity Generation Details](activity_generators/README.md)** - Understanding activity simulation
- **[Analysis Suite Guide](analyzers/README.md)** - Complete analysis capabilities and interpretation
- **[Export & Documentation](data_exporter/README.md)** - Export formats and report generation
- **[Core Infrastructure](core/README.md)** - Workflow management and advanced features
- **[Employee Generation](employee_generator/README.md)** - Employee profile creation process
- **[Utils & Constants](utils/README.md)** - System constants and configuration values

## 🆘 Troubleshooting

### Performance Issues
- **Large datasets** (5000+ employees): Use `--quiet` mode and ensure sufficient RAM
- **Long generation times**: Consider reducing days or using smaller employee counts for testing
- **Memory errors**: Split large datasets into multiple smaller runs

### Common Errors
- **Missing columns in analysis mode**: Check that your CSV has required fields (see [analyzers documentation](analyzers/README.md))
- **Invalid parameters**: Use `--help` to see valid ranges for all parameters
- **File permissions**: Ensure write access to output directory

**Still need help?** Check the [Technical Architecture Overview](TECHNICAL_OVERVIEW.md) or specific module documentation above.
