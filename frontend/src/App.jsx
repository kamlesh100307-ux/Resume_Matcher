
import { useEffect, useState } from 'react'

const API = 'http://127.0.0.1:8000'

export default function App() {
  const [page, setPage] = useState('login')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [activeUser, setActiveUser] = useState('')
  const [jobs, setJobs] = useState([])
  const [role, setRole] = useState('')
  const [experience, setExperience] = useState('0')
  const [resume, setResume] = useState(null)
  const [result, setResult] = useState(null)
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetch(`${API}/jobs`)
      .then(response => response.json())
      .then(data => {
        setJobs(data)

        if (data.length) {
          setRole(data[0].title)
        }
      })
      .catch(() => {
        setMessage('Cannot connect to backend. Start FastAPI first.')
      })
  }, [])

  async function accountSubmit(event) {
    event.preventDefault()
    setMessage('')

    const endpoint =
      page === 'register' ? '/register' : '/login'

    try {
      const response = await fetch(`${API}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username,
          password
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Request failed')
      }

      if (page === 'register') {
        setMessage('Registered successfully. Please log in.')
        setPage('login')
      } else {
        setActiveUser(data.username)
        setPage('analyzer')
        setMessage('')
      }

      setPassword('')
    } catch (error) {
      setMessage(error.message || 'Could not connect to backend')
    }
  }

  async function analyzeSubmit(event) {
    event.preventDefault()

    if (!resume) {
      setMessage('Please select a PDF or DOCX resume.')
      return
    }

    const form = new FormData()

    form.append('role', role)
    form.append('experience', experience)
    form.append('resume', resume)

    setLoading(true)
    setMessage('')
    setResult(null)

    try {
      const response = await fetch(`${API}/analyze`, {
        method: 'POST',
        body: form
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Analysis failed')
      }

      setResult(data)
    } catch (error) {
      setMessage(error.message || 'Could not analyze resume')
    } finally {
      setLoading(false)
    }
  }

  function logout() {
    setActiveUser('')
    setResult(null)
    setResume(null)
    setPage('login')
    setMessage('Logged out.')
  }

  return (
    <main className="page">
      <header className="topbar">
        <div className="brand">
          Resume<span>Match</span>
        </div>

        {activeUser && (
          <div className="userbar">
            Hi, {activeUser}

            <button
              className="button secondary small"
              onClick={logout}
            >
              Logout
            </button>
          </div>
        )}
      </header>

      {page !== 'analyzer' ? (
        <section className="auth-card">
          <p className="eyebrow">CAREER TOOL</p>

          <h1>
            {page === 'register'
              ? 'Create your account'
              : 'Find your role match'}
          </h1>

          <p className="muted">
            {page === 'register'
              ? 'Register to try the resume matching demo.'
              : 'Log in to analyze your resume against a job role.'}
          </p>

          <form
            onSubmit={accountSubmit}
            className="form"
          >
            <label>Username</label>

            <input
              value={username}
              onChange={event => setUsername(event.target.value)}
              minLength="3"
              required
            />

            <label>Password</label>

            <input
              type="password"
              value={password}
              onChange={event => setPassword(event.target.value)}
              minLength="6"
              required
            />

            <button className="button">
              {page === 'register' ? 'Register' : 'Login'}
            </button>
          </form>

          <p className="switch">
            {page === 'register'
              ? 'Already have an account?'
              : "Don't have an account?"}

            {' '}

            <button
              className="text-button"
              onClick={() => {
                setPage(page === 'register' ? 'login' : 'register')
                setMessage('')
              }}
            >
              {page === 'register' ? 'Login' : 'Register'}
            </button>
          </p>
        </section>
      ) : (
        <section className="content">
          <div className="intro">
            <p className="eyebrow">RESUME ANALYZER</p>

            <h1>
              Find out how your resume matches a role.
            </h1>

            <p className="muted">
              Choose a role, enter your experience, and upload your resume.
            </p>
          </div>

          <form
            className="analyzer-card form"
            onSubmit={analyzeSubmit}
          >
            <label>Target job role</label>

            <select
              value={role}
              onChange={event => setRole(event.target.value)}
              required
            >
              {jobs.map(job => (
                <option
                  key={job.id}
                  value={job.title}
                >
                  {job.title}
                </option>
              ))}
            </select>

            <label>Your years of experience</label>

            <input
              type="number"
              min="0"
              max="60"
              step="0.5"
              value={experience}
              onChange={event => setExperience(event.target.value)}
              required
            />

            <label>Resume (PDF/DOCX, max 5 MB)</label>

            <input
              type="file"
              accept=".pdf,.docx"
              onChange={event => {
                setResume(event.target.files[0] || null)
              }}
              required
            />

            <button
              className="button"
              disabled={loading || !jobs.length}
            >
              {loading ? 'Analyzing...' : 'Analyze resume'}
            </button>
          </form>

          {result && (
            <section className="result-card">
              <div className="result-heading">
                <div>
                  <p className="eyebrow">MATCH RESULT</p>
                  <h2>{result.job_title}</h2>
                </div>

                <div className="score">
                  {result.match_percentage}%
                </div>
              </div>

              <div className="progress">
                <div
                  style={{
                    width: `${result.match_percentage}%`
                  }}
                />
              </div>

              <div className="score-grid">
                <div>
                  <span>Skill score</span>
                  <strong>{result.skill_score}%</strong>
                </div>

                <div>
                  <span>Experience score</span>
                  <strong>{result.experience_score}%</strong>
                </div>

                <div>
                  <span>Required experience</span>
                  <strong>{result.required_experience}</strong>
                </div>
              </div>

              <div className="skill-columns">
                <div>
                  <h3>
                    Matched skills ({result.matched_skills.length})
                  </h3>

                  {result.matched_skills.length ? (
                    <div className="tags">
                      {result.matched_skills.map(skill => (
                        <span
                          className="tag good"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="muted">
                      No required skills detected.
                    </p>
                  )}
                </div>

                <div>
                  <h3>
                    Skills to improve ({result.missing_skills.length})
                  </h3>

                  {result.missing_skills.length ? (
                    <div className="tags">
                      {result.missing_skills.map(skill => (
                        <span
                          className="tag missing"
                          key={skill}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  ) : (
                    <p className="muted">
                      All listed skills were detected.
                    </p>
                  )}
                </div>
              </div>

              <p className="note">{result.note}</p>
            </section>
          )}
        </section>
      )}

      {message && (
        <div
          className="message"
          role="status"
        >
          {message}
        </div>
      )}

      <footer>
        ResumeMatch · Resume-to-job compatibility demo
      </footer>
    </main>
  )
}
