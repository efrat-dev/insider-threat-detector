# 🛡️ Advanced Insider Threat Dataset Generator

> Professional-grade synthetic dataset generator for cybersecurity research and security testing

## What is this?

This tool generates **classified environment datasets** specifically designed for insider threat research in secure organizations. Unlike generic employee data generators, this system models **classified document handling, security clearance levels, and sensitive operational activities** that are critical for understanding insider threats in government agencies, defense contractors, and high-security enterprises.

### 🔐 **Unique Classification Features**
- **Multi-Level Security Classifications** (Levels 1-4) for employees and documents
- **Classified Document Burning** simulation with security level tracking
- **Clearance-Based Access Patterns** reflecting real security protocols
- **Hostile Country Travel** tracking with security implications
- **Cross-Classification Activities** modeling unauthorized access scenarios

## 🚀 Quick Start

```bash
# Basic dataset generation
python main.py --employees 1000 --days 180

# With noise injection for realism
python main.py --employees 500 --days 90 --add-noise --malicious-ratio 0.08

# Analysis only mode
python main.py --analysis-only --input-file existing_data.csv
```

## 🏗️ How It Works

1. **Employee Profiles** → Creates realistic employee profiles with departments, roles, and characteristics
2. **Behavioral Simulation** → Generates daily activities (building access, printing, document burning, travel)
3. **Analysis & Insights** → Performs comprehensive behavioral and security analysis
4. **Export & Documentation** → Outputs data in CSV/Excel with detailed documentation

## 📊 Sample Output

The generator creates **classified environment datasets** with 40+ security-focused features:

```csv
employee_id,date,employee_classification,is_malicious,avg_request_classification,max_request_classification,num_burn_requests,hostile_country_trip,...
001,2024-01-01,3,0,2.5,4,2,0,...
002,2024-01-01,4,1,3.8,4,5,1,...
```

### 🔐 **Security-Specific Data Fields**
- **Employee Security Clearance** (Levels 1-4)
- **Document Classification Levels** (average and maximum per activity)
- **Classified Document Destruction** with volume and classification tracking
- **Security Risk Indicators** including hostile country travel and cross-classification access
- **Clearance-Based Activity Patterns** reflecting security protocol compliance

## 🎯 Use Cases

### 🔬 **Classified Environment Research**
- **Government Agency Studies**: Insider threat patterns in classified environments
- **Defense Contractor Analysis**: Security clearance-based behavioral modeling
- **Intelligence Community Research**: Multi-level security access pattern analysis

### 🛡️ **Security Applications**
- **Clearance Violation Detection**: Training algorithms to detect unauthorized access
- **Classification Leak Prevention**: Modeling document exfiltration scenarios
- **Security Protocol Testing**: Validating clearance-based access controls
- **Insider Threat Training**: Realistic scenarios for security awareness programs

### 💼 **Specialized Applications**
- **Security Audit Preparation**: Test data for classified environment audits
- **Compliance Testing**: DCID 6/3, ICD 503, and other security standard validation
- **Risk Assessment Models**: Development of clearance-based risk scoring systems

## 📁 Project Structure

- **[Employee Generator](employee_generator/)** - Creates realistic employee profiles and organizational structures
- **[Activity Generators](activity_generators/)** - Simulates daily employee activities and behaviors
- **[Analyzers](analyzers/)** - Performs behavioral and security analysis on generated data
- **[Data Export](data_exporter/)** - Exports datasets with comprehensive documentation
- **[Configuration](config/)** - Manages behavioral patterns and organizational settings
- **[Core Infrastructure](core/)** - Workflow management and system utilities
- **[CLI Interface](cli/)** - Command-line tools and user interface

## 📚 Documentation

### 📖 **Getting Started Guides**
- **[🏗️ Technical Architecture Overview](TECHNICAL_OVERVIEW.md)** - System design and data flow
- **[📖 User Guide & Quick Reference](USER_GUIDE.md)** - Practical usage guide with examples
- **[📊 Dataset Schema & Field Definitions](DATA_SCHEMA.md)** - Complete dataset structure documentation

### 🔧 **Module Documentation**
- **[Complete Usage Guide](cli/README.md)** - Detailed command-line options and examples
- **[Configuration Guide](config/README.md)** - Customizing behavioral patterns and settings
- **[Analysis Features](analyzers/README.md)** - Understanding analysis outputs and metrics
- **[Technical Architecture](core/README.md)** - System design and workflow details

## 🛠️ Requirements

- Python 3.8+
- pandas, numpy, openpyxl
- 50MB+ free disk space
- 1GB+ RAM for large datasets (5000+ employees)

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

---

**Ready to generate your first insider threat dataset?** Start with `python main.py --help` for full options.
