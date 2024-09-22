# core/templates.py

cv_template = r"""
                    \documentclass[a4paper,9pt]{article}
                    \usepackage{hyperref}
                    \usepackage[margin=0.7in]{geometry}
                    \usepackage{enumitem}
                    \usepackage{titlesec}

                    % Define the format for section titles
                    \titleformat{\section}{\bfseries\Large}{}{0em}{}[\titlerule]
                    \titleformat{\subsection}{\bfseries\large}{}{0em}{}
                    # \titlespacing*{\section}{0pt}{0.5ex plus 0.2ex minus 0.2ex}{0.5ex plus 0.2ex}
                    

                    \begin{document}

                    \pagestyle{empty} % Avoid page number

                    % Personal Information
                    \begin{center}
                        {\LARGE \textbf{Jane Doe}} \\
                        \vspace{0.2cm}
                        New York, USA | +1 123 456 7890 | \href{mailto:jane.doe@example.com}{jane.doe@example.com} | \href{https://www.linkedin.com/in/janedoe}{LinkedIn}
                    \end{center}

                    % Professional Summary
                    \section*{Professional Summary}
                    Detail-oriented Data Analyst with 4+ years of experience in interpreting and analyzing data to drive successful business solutions. Proficient in data visualization, data mining, and predictive modeling. Skilled in SQL, Python, and data visualization tools such as Tableau and Power BI. Adept at leveraging analytical skills to solve complex business problems and enhance decision-making processes.

                    % Education Section
                    \section*{Education}
                    \textbf{New York University} \\
                    \textbf{Master of Science in Data Science} \hfill Sep 2019 - May 2021
                    \begin{itemize}[left=0em]
                        \item Completed coursework in Machine Learning, Data Mining, and Big Data Analytics.
                        \item Thesis: “Predictive Analytics for Customer Churn in the Retail Sector.”
                    \end{itemize}

                    \textbf{University of California, Berkeley} \\
                    \textbf{Bachelor of Science in Statistics} \hfill Sep 2015 - May 2019
                    \begin{itemize}[left=0em]
                        \item Graduated with honors, with a focus on probability, statistical inference, and data visualization.
                    \end{itemize}

                    % Professional Experience Section
                    \section*{Professional Experience}
                    \textbf{XYZ Corporation, New York, USA} \\
                    \textbf{Data Analyst} \hfill Jun 2021 - Present
                    \begin{itemize}[left=0em]
                        \item Analyzed customer behavior data to identify key trends, increasing customer retention by 15\%.
                        \item Developed interactive dashboards using Tableau to provide actionable insights for the marketing team.
                        \item Conducted A/B testing and statistical analysis to evaluate marketing campaigns, leading to a 20\% increase in ROI.
                        \item Automated data extraction and transformation processes, reducing report generation time by 40\%.
                    \end{itemize}

                    \textbf{ABC Tech, San Francisco, USA} \\
                    \textbf{Junior Data Analyst} \hfill Jun 2019 - May 2021
                    \begin{itemize}[left=0em]
                        \item Assisted in the development of predictive models to optimize supply chain management, reducing stockouts by 30\%.
                        \item Collaborated with cross-functional teams to design data collection strategies and improve data quality.
                        \item Created monthly reports for stakeholders, summarizing key metrics and data insights.
                    \end{itemize}

                    % Skills Section
                    \section*{Skills}
                    \textbf{Technical:} SQL (MySQL, PostgreSQL), Python (Pandas, NumPy, Scikit-learn, Matplotlib), R, Tableau, Power BI, Excel (Advanced), Git. \\
                    \textbf{Analytical:} Data visualization, statistical analysis, predictive modeling, machine learning, A/B testing, data mining. \\
                    \textbf{Languages:} English (Fluent), Spanish (Intermediate). \\
                    \textbf{Soft Skills:} Problem-solving, communication, teamwork, attention to detail, adaptability.

                    % Flexible Section (change this name according to the needs)
                    \section*{Flexible Section}
                    \textbf{Projects:} Customer Segmentation using clustering techniques (K-Means, DBSCAN), Predictive Modeling for sales forecasting (ARIMA, Prophet), Real-time Data Streaming for anomaly detection (Kafka, Spark Streaming) \\
                    \textbf{Publications:} "Machine Learning in Financial Risk Analysis" (Journal of Finance, 2021), "Deep Learning for Natural Language Processing" (Data Science Review, 2020), "Big Data Analytics in Healthcare" (Health Informatics Conference, 2019) \\
                    \textbf{Certifications:} AWS Certified Machine Learning Specialty (2020), Google Professional Data Engineer (2019), Microsoft Certified: Azure AI Engineer Associate (2021) \\
                    \textbf{Interests:} Data Privacy and Ethics, Quantum Computing, Data Visualization (Tableau, D3.js), Personal: Guitar playing, Cooking, Scuba diving \\


                    \end{document}

                    """

cover_letter_template = r"""
\documentclass[a4paper,12pt]{article}
\usepackage{hyperref}
\usepackage[margin=1in]{geometry}
\usepackage{enumitem}
\usepackage{titlesec}

% Define the format for section titles
\titleformat{\section}{\bfseries\Large}{}{0em}{}[\titlerule]
\titleformat{\subsection}{\bfseries\large}{}{0em}{}
%\titlespacing*{\section}{0pt}{0.5ex plus 0.2ex minus 0.2ex}{0.5ex plus 0.2ex}

\pagestyle{empty} % Avoid page number

\begin{document}

\begin{center}
    {\LARGE \textbf{Jane Doe}} \\ % Your name
    \vspace{0.2cm}
    New York, NY | (123) 456-7890 | \href{mailto:jane.doe@example.com}{jane.doe@example.com} \\
    \href{https://www.linkedin.com/in/janedoe}{LinkedIn}
\end{center}

\vspace{0.5cm} % Vertical space between contact information and date

September 20, 2024

Hiring Manager \\
Data Solutions Inc.

\vspace{0.5cm} % Vertical space before the opening

\textbf{Dear Hiring Manager,}

I am writing to express my strong interest in the Data Analyst position at Data Solutions Inc. As a recent graduate with a Master’s degree in Data Science from New York University and a passion for turning data into impactful business decisions, I am excited about the opportunity to contribute to your team’s success. \par\vspace{0.5cm}\par

During my academic career, I developed a comprehensive skill set in statistical analysis, data visualization, and programming languages such as Python and SQL. I have successfully applied these skills to several real-world projects, including a predictive analytics model for customer churn that achieved an 87\% accuracy rate. My hands-on experience in analyzing complex datasets, building predictive models, and presenting data-driven insights has prepared me well for this role. \par\vspace{0.5cm}\par

What truly sets me apart is my ability to bridge the gap between technical data analysis and strategic business decisions. I believe that effective data analysis is not just about understanding the numbers but about transforming those numbers into a narrative that drives strategic growth. My previous internship at XYZ Corp taught me the importance of clear communication, as I worked closely with cross-functional teams to develop data-driven solutions that increased operational efficiency by 20\%. I am eager to bring this unique blend of technical expertise and business acumen to Data Solutions Inc. \par\vspace{0.5cm}\par

Moreover, I thrive in dynamic, fast-paced environments. My experience working on collaborative projects, such as developing a sales forecasting dashboard for a leading retail client, showcased my ability to work under pressure and meet tight deadlines without compromising on quality. I am confident that my proactive approach and problem-solving mindset will allow me to make a significant contribution to your team from day one. \par\vspace{0.5cm}\par

I am genuinely excited about the prospect of joining Data Solutions Inc. and leveraging my skills to support your data-driven initiatives. I am confident that my technical skills, analytical mindset, and passion for data analysis make me a strong candidate for this role. I would welcome the opportunity to discuss how my background and qualifications align with your team’s needs in more detail. \par\vspace{0.5cm}\par

Thank you for considering my application. I look forward to the possibility of contributing to the continued success of Data Solutions Inc.

\vspace{0.5cm} % Vertical space before the closing

\textbf{Sincerely,} \\
\textbf{Jane Doe}

\end{document}


                    """