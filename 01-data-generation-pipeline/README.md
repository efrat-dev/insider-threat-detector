# 🛡️ Advanced Insider Threat Dataset Generator

> Professional-grade synthetic dataset generator for cybersecurity research and security testing

## What is this?

This tool generates realistic employee activity datasets for insider threat research, security training, and anomaly detection system development. It creates synthetic data that mimics real organizational behavior patterns while maintaining privacy and security.

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

The generator creates datasets with 40+ features including:
- Building access patterns (entry/exit times, multi-campus access)
- Document activities (printing volume, secure destruction)
- Travel patterns (business trips, hostile country visits)
- Risk indicators (off-hours activity, suspicious combinations)

## 🎯 Use Cases

- **🔬 Research**: Academic insider threat studies and behavioral analysis
- **🛡️ Security**: Training datasets for detection algorithms and security tools
- **💼 Business**: HR analytics, system testing, and compliance scenarios
- **🎓 Education**: Cybersecurity training and simulation exercises

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
