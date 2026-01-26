import { useEffect, useState } from "react";
import "../App.css";

type Job = {
  title: string;
  company: string;
  location: string;
  source: string;
  url: string;
};

const Jobs = () => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/jobs")
      .then((res) => res.json())
      .then((data) => {
        setJobs(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="page">
      <h1 className="title">Carevia Job Portal</h1>

      <div className="search">
        <input placeholder="Search jobs (Python, React, Backend...)" />
      </div>

      {loading && <p>Loading jobs...</p>}
      {!loading && jobs.length === 0 && <p>No jobs found</p>}

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
