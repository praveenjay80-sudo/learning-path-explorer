
TAXONOMY = [
  ("Mathematics", "#7c3aed", [
    ("Algebra", ["Abstract Algebra","Linear Algebra","Commutative Algebra","Lie Theory","Representation Theory","Homological Algebra","Category Theory","Universal Algebra","K-Theory"]),
    ("Analysis", ["Real Analysis","Complex Analysis","Functional Analysis","Harmonic Analysis","Measure Theory","Numerical Analysis","Operator Theory","Convex Analysis","Several Complex Variables"]),
    ("Geometry", ["Euclidean Geometry","Differential Geometry","Riemannian Geometry","Algebraic Geometry","Symplectic Geometry","Geometric Group Theory","Metric Geometry","Discrete Geometry"]),
    ("Topology", ["General Topology","Algebraic Topology","Differential Topology","Geometric Topology","Low-Dimensional Topology","Knot Theory","Homotopy Theory","Topological Data Analysis"]),
    ("Number Theory", ["Elementary Number Theory","Algebraic Number Theory","Analytic Number Theory","Arithmetic Geometry","Modular Forms & Automorphic Forms","Computational Number Theory","Diophantine Geometry"]),
    ("Discrete Mathematics", ["Combinatorics","Graph Theory","Coding Theory","Cryptography","Discrete Optimization","Probabilistic Combinatorics","Combinatorial Geometry","Matroid Theory"]),
    ("Applied Mathematics", ["Dynamical Systems","Mathematical Physics","Optimization Theory","Control Theory","Mathematical Biology","Mathematical Finance","Fluid Dynamics Mathematics","Game Theory"]),
    ("Statistics & Probability", ["Probability Theory","Statistical Inference","Stochastic Processes","Bayesian Statistics","Time Series Analysis","Multivariate Statistics","High-Dimensional Statistics","Causal Inference"]),
    ("Logic & Foundations", ["Mathematical Logic","Set Theory","Model Theory","Proof Theory","Computability Theory","Type Theory","Descriptive Set Theory"]),
  ]),

  ("Physics", "#1d4ed8", [
    ("Classical Mechanics", ["Newtonian Mechanics","Lagrangian Mechanics","Hamiltonian Mechanics","Rigid Body Dynamics","Continuum Mechanics","Nonlinear Dynamics","Celestial Mechanics"]),
    ("Quantum Physics", ["Quantum Mechanics","Quantum Field Theory","Quantum Information Theory","Quantum Optics","Many-Body Physics","Quantum Thermodynamics","Open Quantum Systems"]),
    ("Electromagnetism", ["Classical Electrodynamics","Optics","Photonics","Plasma Physics","Nonlinear Optics","Metamaterials"]),
    ("Condensed Matter Physics", ["Solid State Physics","Superconductivity","Magnetism","Topological Matter","Strongly Correlated Systems","Soft Matter Physics","Nanophysics"]),
    ("Thermodynamics & Statistical Mechanics", ["Classical Thermodynamics","Statistical Mechanics","Phase Transitions & Critical Phenomena","Non-Equilibrium Physics","Kinetic Theory","Stochastic Thermodynamics"]),
    ("Relativity & Cosmology", ["Special Relativity","General Relativity","Cosmology","Gravitational Waves","Black Hole Physics","Quantum Gravity"]),
    ("Nuclear & Particle Physics", ["Nuclear Structure","Nuclear Reactions","Standard Model of Particle Physics","Particle Phenomenology","Neutrino Physics","Beyond Standard Model"]),
    ("Atomic & Molecular Physics", ["Atomic Physics","Molecular Physics","Laser Physics","Spectroscopy","Cold Atoms & Quantum Gases","Ultrafast Physics"]),
  ]),

  ("Chemistry", "#15803d", [
    ("Organic Chemistry", ["Reaction Mechanisms","Organic Synthesis","Stereochemistry","Natural Products Chemistry","Medicinal Chemistry","Organometallic Chemistry","Supramolecular Chemistry"]),
    ("Inorganic Chemistry", ["Coordination Chemistry","Solid State Chemistry","Bioinorganic Chemistry","Main Group Chemistry","Inorganic Materials","Cluster Chemistry"]),
    ("Physical Chemistry", ["Chemical Thermodynamics","Chemical Kinetics","Quantum Chemistry","Electrochemistry","Surface Chemistry","Molecular Spectroscopy","Chemical Dynamics"]),
    ("Analytical Chemistry", ["Chromatography & Separation","Spectroscopic Analysis","Electroanalysis","Mass Spectrometry","Structural Analysis","Chemometrics"]),
    ("Computational Chemistry", ["Density Functional Theory","Molecular Dynamics Simulation","Molecular Modeling & Docking","Materials Simulation","Cheminformatics"]),
    ("Environmental Chemistry", ["Atmospheric Chemistry","Aquatic Chemistry","Green Chemistry","Soil Chemistry","Environmental Toxicology"]),
    ("Polymer & Materials Chemistry", ["Polymer Synthesis","Polymer Physics","Nanomaterials Chemistry","Functional Materials","Soft Materials"]),
    ("Biochemistry", ["Protein Chemistry","Nucleic Acid Chemistry","Metabolic Biochemistry","Lipid Biochemistry","Chemical Biology"]),
  ]),

  ("Biology & Life Sciences", "#b45309", [
    ("Cell Biology", ["Cell Structure & Organelles","Cell Signaling","Cell Cycle & Division","Membrane Biology","Intracellular Transport","Autophagy & Proteostasis"]),
    ("Genetics & Genomics", ["Classical Genetics","Molecular Genetics","Genomics & Transcriptomics","Population Genetics","Epigenetics","Single-Cell Genomics"]),
    ("Molecular Biology", ["Gene Expression & Regulation","DNA Biology & Repair","RNA Biology","Protein Biology","Synthetic Biology","CRISPR & Genome Editing"]),
    ("Ecology", ["Community Ecology","Ecosystem Ecology","Landscape Ecology","Marine Ecology","Soil Ecology","Microbial Ecology","Urban Ecology"]),
    ("Evolutionary Biology", ["Natural Selection & Adaptation","Speciation","Phylogenetics","Evolutionary Genetics","Macroevolution","Evo-Devo"]),
    ("Microbiology", ["Bacteriology","Virology","Mycology","Parasitology","Antimicrobial Resistance","Environmental Microbiology"]),
    ("Neuroscience", ["Cellular Neuroscience","Systems Neuroscience","Cognitive Neuroscience","Molecular Neuroscience","Computational Neuroscience","Clinical Neuroscience"]),
    ("Plant Biology", ["Plant Physiology","Plant Genetics & Breeding","Plant Ecology","Plant Pathology","Plant Development"]),
    ("Animal Biology", ["Animal Physiology","Comparative Biology","Behavioral Biology","Zoology","Conservation Biology"]),
    ("Developmental Biology", ["Embryology","Developmental Genetics","Stem Cell Biology","Tissue Regeneration","Aging Biology"]),
  ]),

  ("Earth & Environmental Sciences", "#374151", [
    ("Geology", ["Mineralogy & Petrology","Structural Geology","Stratigraphy","Geomorphology","Volcanology","Geochronology","Sedimentology"]),
    ("Atmospheric Science", ["Meteorology","Atmospheric Chemistry","Climate Dynamics","Boundary Layer Meteorology","Atmospheric Radiation","Tropical Meteorology"]),
    ("Oceanography", ["Physical Oceanography","Chemical Oceanography","Marine Biology & Ecology","Polar Oceanography","Ocean-Atmosphere Interaction"]),
    ("Environmental Science", ["Environmental Toxicology","Ecosystem Services","Environmental Policy","Pollution Science","Environmental Monitoring"]),
    ("Climatology", ["Climate Change Science","Paleoclimatology","Climate Modeling","Biogeochemistry","Climate Risk & Adaptation"]),
    ("Geophysics", ["Seismology","Geomagnetism","Geodesy","Exploration Geophysics","Geodynamics"]),
    ("Hydrology", ["Surface Hydrology","Groundwater Hydrology","Ecohydrology","Glaciology","Urban Hydrology"]),
    ("Soil Science", ["Soil Physics","Soil Chemistry","Soil Biology","Soil Classification","Land Degradation & Restoration"]),
  ]),

  ("Astronomy & Space Science", "#b91c1c", [
    ("Stellar Astrophysics", ["Stellar Structure & Evolution","Star Formation","Variable & Binary Stars","Compact Objects","Stellar Populations & Chemical Evolution"]),
    ("Planetary Science", ["Solar System Formation","Planetary Geology","Planetary Atmospheres","Small Bodies","Astrobiology"]),
    ("Cosmology", ["Big Bang Theory","Dark Matter & Dark Energy","Large-Scale Structure","Observational Cosmology","Theoretical Cosmology"]),
    ("Galactic Astronomy", ["Milky Way Structure & Dynamics","Galaxy Formation & Evolution","Active Galactic Nuclei","Galaxy Clusters","Interstellar Medium"]),
    ("Observational Astronomy", ["Radio Astronomy","X-Ray & Gamma-Ray Astronomy","Gravitational Wave Astronomy","Exoplanet Detection","Astronomical Instrumentation"]),
    ("Solar Physics", ["Solar Structure","Solar Wind & Heliosphere","Space Weather","Helioseismology","Solar-Terrestrial Relations"]),
  ]),

  ("Computer Science", "#be185d", [
    ("Algorithms & Complexity", ["Algorithm Design","Computational Complexity","Data Structures","Graph Algorithms","Randomized Algorithms","Approximation Algorithms"]),
    ("Machine Learning", ["Supervised Learning","Deep Learning","Reinforcement Learning","Unsupervised & Self-Supervised Learning","Learning Theory","Federated Learning"]),
    ("Natural Language Processing", ["Language Models","Text Classification & NER","Machine Translation","Information Extraction","Dialogue Systems","Computational Linguistics"]),
    ("Computer Vision", ["Image Recognition","Object Detection","3D Vision","Video Understanding","Generative Visual Models"]),
    ("Systems & Architecture", ["Computer Architecture","Operating Systems","Distributed Systems","Cloud & Edge Computing","Embedded Systems","High-Performance Computing"]),
    ("Networks & Security", ["Network Protocols","Cryptography","Cybersecurity","Wireless & Mobile Networks","Network Science"]),
    ("Databases & Data Systems", ["Relational & SQL Databases","NoSQL & NewSQL","Data Mining","Big Data & Stream Processing","Information Retrieval","Knowledge Graphs"]),
    ("Software Engineering", ["Software Architecture","Program Analysis & Verification","Testing & Quality","Programming Languages","DevOps & Reliability"]),
    ("Human-Computer Interaction", ["Interaction Design & UX","Usability & Accessibility","Virtual & Augmented Reality","Social Computing","Wearable Computing"]),
    ("Theoretical Computer Science", ["Automata & Formal Languages","Logic in Computer Science","Quantum Computing","Computational Geometry","Information Theory"]),
  ]),

  ("Engineering", "#0f766e", [
    ("Electrical Engineering", ["Circuit Theory","Signal Processing","Power Systems","VLSI & Microelectronics","Communications Engineering","Control Systems"]),
    ("Mechanical Engineering", ["Solid Mechanics","Fluid Dynamics","Thermodynamics & Heat Transfer","Vibrations & Dynamics","Manufacturing Engineering","Tribology"]),
    ("Civil Engineering", ["Structural Engineering","Geotechnical Engineering","Transportation Engineering","Water Resources Engineering","Construction Management"]),
    ("Chemical Engineering", ["Transport Phenomena","Reaction Engineering","Process Design & Control","Separation Processes","Biochemical Engineering"]),
    ("Materials Engineering", ["Metals & Alloys","Ceramics & Glasses","Polymer Engineering","Electronic Materials","Biomaterials","Composite Materials"]),
    ("Aerospace Engineering", ["Aerodynamics","Propulsion","Aerostructures","Flight Mechanics","Spacecraft Engineering","Orbital Mechanics"]),
    ("Biomedical Engineering", ["Biomechanics","Medical Devices","Neural Engineering","Tissue Engineering","Medical Imaging Engineering"]),
    ("Environmental Engineering", ["Water & Wastewater Treatment","Air Quality Engineering","Solid Waste Management","Sustainable Engineering","Remediation Technology"]),
    ("Robotics & Mechatronics", ["Robot Kinematics & Dynamics","Control Theory","Autonomous Systems","Human-Robot Interaction","Mechatronics"]),
  ]),

  ("Medicine & Health Sciences", "#0369a1", [
    ("Internal Medicine", ["Cardiology","Pulmonology","Gastroenterology","Nephrology","Endocrinology","Rheumatology","Hematology"]),
    ("Oncology", ["Cancer Biology","Medical Oncology","Radiation Oncology","Hematologic Malignancies","Cancer Immunotherapy","Precision Oncology"]),
    ("Neurology & Psychiatry", ["Clinical Neurology","Psychiatry","Neurodegenerative Diseases","Neuropsychiatry","Psychopharmacology","Child & Adolescent Psychiatry"]),
    ("Infectious Diseases", ["Bacteriology & Sepsis","Virology & Emerging Infections","Tropical Medicine","Immunology & Vaccines","Antimicrobial Resistance"]),
    ("Surgery", ["General Surgery","Orthopedic Surgery","Cardiovascular Surgery","Neurosurgery","Minimally Invasive Surgery"]),
    ("Pharmacology", ["Drug Discovery","Pharmacokinetics & Pharmacodynamics","Toxicology","Clinical Pharmacology","Pharmacogenomics"]),
    ("Epidemiology & Public Health", ["Epidemiology","Global Health","Health Policy & Economics","Preventive Medicine","Biostatistics"]),
    ("Medical Imaging & Diagnostics", ["Radiology","Nuclear Medicine","Medical Image Analysis","Pathology","Point-of-Care Diagnostics"]),
    ("Genetics & Precision Medicine", ["Medical Genetics","Gene Therapy","Precision Medicine","Rare Diseases","Pharmacogenomics"]),
  ]),

  ("Social Sciences", "#7c2d12", [
    ("Economics", ["Microeconomics","Macroeconomics","Econometrics","Development Economics","Behavioral Economics","Financial Economics","Labor Economics"]),
    ("Psychology", ["Cognitive Psychology","Social Psychology","Clinical Psychology","Developmental Psychology","Neuropsychology","Personality Psychology"]),
    ("Sociology", ["Social Theory","Social Stratification","Organizational Sociology","Urban Sociology","Political Sociology","Medical Sociology"]),
    ("Political Science", ["Comparative Politics","International Relations","Political Theory","Public Policy","Electoral Studies","Security Studies"]),
    ("Anthropology", ["Cultural Anthropology","Biological Anthropology","Archaeology","Linguistic Anthropology","Medical Anthropology"]),
    ("Geography", ["Human Geography","Physical Geography","GIS & Remote Sensing","Urban Geography","Environmental Geography"]),
    ("Education Research", ["Learning Science","Curriculum & Pedagogy","Educational Psychology","Educational Technology","Higher Education"]),
    ("Communication Studies", ["Media Theory","Political Communication","Journalism Studies","Digital Media Studies","Intercultural Communication"]),
  ]),

  ("Humanities", "#4338ca", [
    ("History", ["Ancient History","Medieval History","Early Modern History","Modern History","Contemporary History","Historiography & Historical Methods"]),
    ("Philosophy", ["Epistemology","Metaphysics","Ethics & Moral Philosophy","Philosophy of Mind","Philosophy of Science","Political Philosophy","Aesthetics"]),
    ("Linguistics", ["Phonetics & Phonology","Syntax & Morphology","Semantics & Pragmatics","Sociolinguistics","Historical Linguistics","Psycholinguistics"]),
    ("Literature", ["Literary Theory & Criticism","Comparative Literature","World Literature","Genre Studies","Translation Studies"]),
    ("Art History & Visual Culture", ["Ancient & Medieval Art","Renaissance & Baroque Art","Modern Art","Contemporary Art","Visual Culture Studies"]),
    ("Cultural Studies", ["Cultural Theory","Media & Communication Studies","Postcolonial Studies","Memory & Heritage","Globalization Studies"]),
    ("Religion & Theology", ["Comparative Religion","Christian Theology","Islamic Studies","Buddhist & Asian Studies","Secular & Atheism Studies"]),
    ("Music", ["Music Theory","Music History","Ethnomusicology","Music Psychology","Composition & Sound Design"]),
  ]),

  ("Business & Management", "#065f46", [
    ("Finance", ["Corporate Finance","Investment & Portfolio Theory","Financial Markets","Risk Management","Financial Econometrics","Behavioral Finance"]),
    ("Marketing", ["Consumer Behavior","Digital Marketing","Brand Management","Marketing Strategy","Services Marketing"]),
    ("Operations & Strategy", ["Supply Chain Management","Operations Management","Competitive Strategy","Innovation Management","Business Analytics"]),
    ("Organizational Behavior", ["Leadership","Organizational Psychology","Human Resource Management","Team Dynamics","Organizational Change"]),
    ("Accounting & Auditing", ["Financial Accounting","Managerial Accounting","Auditing","Taxation","Financial Reporting"]),
    ("Entrepreneurship", ["Venture Finance & VC","Startup Ecosystems","Social Entrepreneurship","Business Model Design","International Business"]),
    ("Business Ethics & Law", ["Business Ethics","Corporate Law","Intellectual Property","Contract Law","Regulatory Compliance"]),
    ("Management Information Systems", ["Enterprise Systems","IT Strategy","E-Commerce","Business Intelligence","Cybersecurity Management"]),
  ]),

  ("Agriculture & Food Science", "#92400e", [
    ("Agronomy", ["Crop Physiology","Soil-Crop Interactions","Precision Agriculture","Weed Science","Crop Protection"]),
    ("Plant Breeding & Genetics", ["Crop Genetics","Hybrid Breeding","Marker-Assisted Selection","Genomic Selection","GM Crop Technology"]),
    ("Animal Science", ["Animal Physiology","Livestock Genetics","Animal Nutrition","Animal Health & Welfare","Aquaculture"]),
    ("Food Science & Technology", ["Food Chemistry","Food Processing Technology","Food Safety & Microbiology","Food Nutrition","Sensory Science"]),
    ("Agricultural Biotechnology", ["Plant Genetic Engineering","Biocontrol Agents","Agricultural Genomics","Biofertilizers","Metabolic Engineering in Plants"]),
    ("Agroecology & Sustainability", ["Sustainable Farming Systems","Agroforestry","Organic Agriculture","Food Systems","Climate-Smart Agriculture"]),
    ("Post-Harvest Technology", ["Post-Harvest Physiology","Food Packaging","Storage Technology","Food Supply Chain Management"]),
  ]),
]

import json

lines = ["const ACADEMIC_TAXONOMY = ["]
total = 0
for domain_name, color, fields in TAXONOMY:
    lines.append(f'  {{name:{json.dumps(domain_name)},color:{json.dumps(color)},fields:[')
    for field_name, subfields in fields:
        sf_objs = ",".join(f'{{name:{json.dumps(sf)},topics:[]}}' for sf in subfields)
        lines.append(f'    {{name:{json.dumps(field_name)},subfields:[{sf_objs}]}},')
        total += len(subfields)
    lines.append(f'  ]}},')
lines.append("];")

output = "\n".join(lines)
print(f"// {total} subfields across {len(TAXONOMY)} domains")

with open("C:/Users/prave/taxonomy.js", "w", encoding="utf-8") as f:
    f.write(output)
print("Written to C:/Users/prave/taxonomy.js")
