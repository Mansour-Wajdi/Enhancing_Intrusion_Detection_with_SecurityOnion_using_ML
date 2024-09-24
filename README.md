# Enhancing Intrusion Detection with SecurityOnion using Machine Learning

## Overview and Context of the project

The work involved the setup and configuration of **[Security Onion](https://securityonionsolutions.com/software)** as a Network Security Monitoring (NSM) solution, developing a machine learning model for alert classification, integrating the ML model with the Security Onion solution filter out false positivea and reduce Alert Fatigue, and creating a graphical user interface (GUI) to streamline the usage of the solution.

This project was conducted as part of an internship at the **[National Agency of Cybersecurity (NACS)](https://www.ancs.tn/)**, or **Agence Nationale de la Cybersécurité (ANCS)** in French, a Tunisian agency specializing in safeguarding digital infrastructures. The primary objective of this project is to enhance the efficiency of Intrusion Detection Systems (IDS) by reducing the number of false positives generated, allowing security analysts to focus on real threats.

## Repository Structure

The repository is organized as follows:

- **App/**: Contains the main application code, including the scripts for network monitoring and machine learning model integration with Security Onion.
- **IPython Notebook/**: Includes Jupyter notebooks for machine learning model development and alert prioritization.
- **report_images/**: Stores images used for documentation purposes.
- **README.md**: Documentation of the project and instructions for setup.

## Tasks Achieved

### 1. Security Onion Setup, Attack Simulation, and Detection Assessment

#### Virtualized Architecture Setup
The virtualized architecture was established using Oracle VirtualBox. Three machines were set up: 
- **Attacking Machine (Kali Linux)**: This machine was used to simulate attacks.
- **Victim Machine (Windows 10)**: This machine contained vulnerabilities to simulate attack scenarios.
- **Security Onion Machine (Ubuntu Server 20.04)**: Hosted Security Onion for monitoring and intrusion detection.
- **Network Configuration**: All three machines were connected to the same NAT Network, establishing a controlled testing environment.

<br>
<img src="report_images/Virtualized_Architecture_topology.svg" alt="Virtualized Architecture topology" width="800"/>
<br>

#### Security Onion Standalone Setup
Security Onion was installed and configured for Network Security Monitoring (NSM) and Enterprise Security Monitoring (ESM). Tools like **Suricata** and **Google Stenographer** were used for intrusion detection and full packet capture.

<br>
<img src="report_images/Installation_options_for_Security_Onion.png" alt="Installation options for Security Onion" width="800"/>
<br>
<img src="report_images/Installation_options_for_Security_Onion2.png" alt="Installation options for Security Onion" width="800"/>
<br>

#### Security Onion Import Setup
...

### 2. Basic Examples of Attack Simulation and Detection
Two attack examples were simulated:
- **Metasploit SMB Exploitation**

<br>
<img src="report_images/Metasploit_exploitation_windows_smb_psexec.png" alt="Metasploit exploitation windows/smb/psexec" width="800"/>
<br>

- **Security Onion detection**

<br>
<img src="report_images/Metasploit_exploitation_windows_smb_results.png" alt="Metasploit exploitation windows/smb/psexec results" width="800"/>
<br>

- **NMAP Scan**

<br>
<img src="report_images/NMAP_scan_execution.png" alt="NMAP scan execution and results" width="800"/>
<br>

- **Security Onion detection**

<br>
<img src="report_images/NMAP_scan_results.png" alt="NMAP scan execution and results" width="800"/>
<br>

### 3. Machine Learning Model Development

#### Classification Model:
This phase of the project centers on the development of a machine learning classification model, trained on the **UNSW-NB15 dataset**, to predict the authenticity of network traffic, distinguishing between genuine threats and false positives.

#### UNSW-NB15 Dataset:
The [UNSW-NB15 Dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset) is a publicly available dataset widely used in cybersecurity to develop and test intrusion detection systems (IDS) and intrusion prevention systems (IPS). It was developed by the Australian Centre for Cyber Security (ACCS) at the University of New South Wales in Australia.

The figure below summarizes the full steps of the ML Model development:

<br>
<img src="report_images/workflow_diagram_for_ML_model_Development.svg" alt="workflow diagram for ML model Development" width="800"/>
<br>

#### Implementation:
The implementation for this step is documented in a Jupyter notebook, offering a step-by-step explanation of the process. Please refer to [Classification model.ipynb](IPython%20Notebook/Classification%20model.ipynb) for access to this detailed guide.

### 4. Alert Prioritization with Packet Analysis and Machine Learning
The alert prioritization process involved four essential steps arranged in a pipeline: 
- **Elasticsearch Data Extraction**
- **PCAP Files Fetching**
- **Feature Extraction**
- **Prediction**

<br>
<img src="report_images/workflow_diagram_for_Alerts_prioritization.svg" alt="workflow diagram for Alerts prioritization" width="800"/>
<br>

#### Elasticsearch Data Extraction:
The first step involves extracting Suricata alerts from **Elasticsearch**, identifying the associated connection information (flow info) for each alert, and saving the results in a CSV file.

<br>
<img src="report_images/Sequence_diagram_for_Elasticsearch_data_extraction.svg" alt="Sequence diagram for Elasticsearch data extraction" width="800"/>
<br>

#### Implementation:
The implementation for this step is documented in a Jupyter notebook, offering a step-by-step explanation of the process. Please refer to [Classification model.ipynb](IPython%20Notebook/Elasticsearch%20Data%20Extraction.ipynb) for access to this detailed guide.
 

#### PCAP Files Fetching:
This step focuses on fetching **Packet Capture (PCAP)** files essential for acquiring the complete network flow associated with each alert. The process involves SSH connectivity with the Security Onion machine.

<br>
<img src="report_images/Sequence_diagram_for_PCAP_Files_Fetching.svg" alt="Sequence diagram for PCAP Files Fetching" width="800"/>
<br>

#### Implementation:
The implementation for this step is documented in a Jupyter notebook, providing a comprehensive, step-by-step explanation of the process. You can access the detailed guide in [Remote PCAP Request and Retrieval (so-standalone).ipynb](IPython%20Notebook/Remote%20PCAP%20Request%20and%20Retrieval%20(so-standalone).ipynb) for the standalone node and in [Remote PCAP Retrieval and Filtering (so-import).ipynb](IPython%20Notebook/Remote%20PCAP%20Retrieval%20and%20Filtering%20(so-import).ipynb) for the import node, each tailored to their respective implementations.


#### Features Extraction:
In this step, features for each alert are computed based on the UNSW-NB15 dataset. The relevant features are extracted from each alert's PCAP file and saved in a CSV file.

<br>
<img src="report_images/Sequence_diagram_for_Features_Extraction.svg" alt="Sequence diagram for Features Extraction" width="800"/>
<br>

#### Prediction:
The final step involves predicting whether the alerts correspond to true attacks or false alarms, using the previously trained classification model.

<br>
<img src="report_images/Sequence_diagram_for_Prediction.svg" alt="Sequence diagram for Prediction" width="800"/>
<br>

#### Implementation:
The implementation for this step is documented in a Jupyter notebook, offering a step-by-step explanation of the process. Please refer to [Predictive Analysis.ipynb](IPython%20Notebook/Predictive%20Analysis.ipynb) for access to this detailed guide.


## Graphical User Interface (GUI) Development
A graphical interface was developed using **CustomTkinter** to facilitate interaction with the system.

### Use Cases:
The diagram below offers a visual representation of the various interaction scenarios, providing a comprehensive understanding of the functionalities and use cases.

<br>
<img src="report_images/Use_Cases.svg" alt="Use Cases" width="800"/>
<br>

### App Interfaces:
1. **Elasticsearch Alerts Interface**: Allows analysts to retrieve Suricata alerts and related flow information.

<br>
<img src="report_images/GUI_Interface_1_Elasticsearch_Alerts.png" alt="GUI Interface 1 Elasticsearch Alerts" width="800"/>
<br>

<br>
<img src="report_images/GUI_Interface_1_Elasticsearch_Alerts_Results.png" alt="GUI Interface 1 Elasticsearch Alerts Results" width="800"/>
<br>

2. **Security Onion Machine Interface**: Enables packet capture retrieval and feature extraction.

<br>
<img src="report_images/GUI_Interface_2_Security_Onion_Host_Machine1.jpg" alt="GUI Interface 2 Security Onion Host Machine" width="800"/>
<br>

<br>
<img src="report_images/GUI_Interface_2_Security_Onion_Host_Machine2.png" alt="GUI Interface 2 Security Onion Host Machine part 2" width="800"/>
<br>

<br>
<img src="report_images/GUI_Interface_2_Security_Onion_Host_Machine_Results.png" alt="GUI Interface 2 Security Onion Host Machine Results" width="800"/>
<br>

3. **Prediction Panel**: Predicts whether an alert is a genuine threat or a false positive.

<br>
<img src="report_images/GUI_Interface_3_Prediction_Panel.png" alt="GUI Interface 3 Prediction Panel" width="800"/>
<br>

<br>
<img src="report_images/GUI_Interface_3_Prediction_Panel_Results.png" alt="GUI Interface 3 Prediction Panel Results" width="800"/>
<br>

4. **Automation Panel**: Automates the alert retrieval and prediction process.

<br>
<img src="report_images/GUI_Interface_4_automation_panel1.png" alt="GUI Interface 4 automation panel" width="800"/>
<br>

<br>
<img src="report_images/GUI_Interface_4_automation_panel2.png" alt="GUI Interface 4 automation panel part 2" width="800"/>
<br>

## Conclusion

This project successfully addressed the challenge of reducing false positives in intrusion detection systems. By integrating machine learning models into the IDS workflow, the project reduced unnecessary alerts and improved the overall efficiency of cybersecurity operations. This work represents a significant step toward enhancing the resilience of digital defenses in a world where cybersecurity threats continue to evolve.

## References
- [ANCS Official Website](https://www.ancs.tn/)
- [Security Onion](https://securityonionsolutions.com/software)
- [Security Onion Documentation](https://docs.securityonion.net/en/2.3/)
- [UNSW-NB15 Dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)
- [VirtualBox User Manual](https://www.virtualbox.org/manual/UserManual.html)
- [Metasploit Documentation](https://docs.metasploit.com/)
- [Nmap Documentation](https://nmap.org/book/man.html)
- [CustomTkinter Documentation](https://customtkinter.tomschimansky.com/documentation/)
