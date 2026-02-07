import { useEffect, useState } from "react";
import config from "../config";
import "../App.css";

type Job = {
  title: string;
  company: string;
  location: string;
  source: string;
  url: string;
  category?: string;
};

const Jobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJobs = async (retries = 3) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${config.apiUrl}/jobs`);

      if (!response.ok) {
        throw new Error(`Failed to fetch jobs: ${response.statusText}`);
      }

      const data = await response.json();
      setJobs(data.jobs || []);
    } catch (err) {
      console.error("Error fetching jobs:", err);

      // Retry logic
      if (retries > 0) {
        console.log(`Retrying... (${retries} attempts left)`);
        setTimeout(() => fetchJobs(retries - 1), 2000);
      } else {
        setError(err instanceof Error ? err.message : "Failed to load jobs");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  return (
    <div className="page">
      <h1 className="title">Carevia Job Portal</h1>

      <div className="search">
        <input placeholder="Search jobs (Python, React, Backend...)" />
      </div>

      {loading && <p>Loading jobs...</p>}

      {error && (
        <div style={{ color: "red", padding: "20px", textAlign: "center" }}>
          <p>Error: {error}</p>
          <button onClick={() => fetchJobs()}>Retry</button>
        </div>
      )}

      {!loading && !error && jobs.length === 0 && <p>No jobs found</p>}

      <div className="jobs-grid">
        {jobs.map((job, index) => (
          <div key={index} className="job-card">
            <div className="job-title">{job.title}</div>
            <div className="job-meta">🏢 {job.company}</div>
            <div className="job-meta">📍 {job.location}</div>
            <div className="job-meta">🌐 {job.source}</div>

            <a
              href={job.url}
              target="_blank"
              rel="noreferrer"
              className="apply-btn"
            >
              Apply →
            </a>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Jobs;
