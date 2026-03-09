-- =============================================
-- MentorMe Database Setup
-- =============================================

IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'mentorme')
    CREATE DATABASE mentorme;
GO

USE mentorme;
GO

-- =============================================
-- DIM CUSTOMER
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'dim_customer')
CREATE TABLE dim_customer (
    customer_id     INT             PRIMARY KEY,
    candidate_name  VARCHAR(100),
    email           VARCHAR(255),
    phone           VARCHAR(20),
    city            VARCHAR(100),
    country         VARCHAR(100),
    education       VARCHAR(50),
    created_at      DATETIME        DEFAULT GETDATE()
);
GO

-- =============================================
-- FACT CV ANALYSIS
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'fact_cv_analysis')
CREATE TABLE fact_cv_analysis (
    analysis_id         BIGINT          PRIMARY KEY,
    customer_id         INT             FOREIGN KEY REFERENCES dim_customer(customer_id),
    status              VARCHAR(20),
    job_role            VARCHAR(100),
    experience_level    VARCHAR(50),
    experience_years    INT,
    overview            VARCHAR(MAX),
    strengths           VARCHAR(MAX),
    gaps                VARCHAR(MAX),
    recommendations     VARCHAR(MAX),
    keywords            VARCHAR(MAX),
    formatting_issues   VARCHAR(MAX),
    regional_insights   VARCHAR(MAX),
    created_at          DATETIME,
    file_name           VARCHAR(255)
);
GO

-- =============================================
-- DIM SKILLS
-- =============================================
IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'dim_skills')
CREATE TABLE dim_skills (
    skill_id        INT             PRIMARY KEY IDENTITY(1,1),
    customer_id     INT             FOREIGN KEY REFERENCES dim_customer(customer_id),
    analysis_id     BIGINT          FOREIGN KEY REFERENCES fact_cv_analysis(analysis_id),
    skill_name      VARCHAR(100),
    skill_type      VARCHAR(20),
    skill_level     VARCHAR(50),
    skill_score     INT,
    created_at      DATETIME        DEFAULT GETDATE()
);
GO



