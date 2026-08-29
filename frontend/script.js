async function analyzeResume() {
  const fileInput = document.getElementById("resumeFile");
  const jobDescription = document.getElementById("jobDescription").value;
  const resultDiv = document.getElementById("result");
  const btn = document.getElementById("analyzeBtn");

  if (!fileInput.files[0] || !jobDescription.trim()) {
    resultDiv.innerHTML = `<p style="color:#b3261e;">Please upload a resume and paste a job description.</p>`;
    return;
  }

  btn.disabled = true;
  btn.innerText = "Analyzing...";
  resultDiv.innerHTML = `<p>⏳ Analyzing your resume...</p>`;

  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);
  formData.append("job_description", jobDescription);

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData,
    });
    const data = await response.json();

    const score = data.match_score_percent;
    let barColor = "#e74c3c";
    if (score >= 60) barColor = "#2ecc71";
    else if (score >= 30) barColor = "#f39c12";

    const matchedTags = data.matched_skills.length
      ? data.matched_skills
          .map((s) => `<span class="tag tag-matched">✓ ${s}</span>`)
          .join("")
      : `<span class="empty-note">No direct matches found</span>`;

    const missingTags = data.missing_skills.length
      ? data.missing_skills
          .map((s) => `<span class="tag tag-missing">✗ ${s}</span>`)
          .join("")
      : `<span class="empty-note">No gaps found — great match!</span>`;

    resultDiv.innerHTML = `
      <div class="score-box">
        <div class="score-number" style="color:${barColor}">${score}%</div>
        <div class="score-label">Resume Match Score</div>
        <div class="bar-bg"><div class="bar-fill" style="width:${score}%; background:${barColor};"></div></div>
      </div>

      <div class="skills-section">
        <div class="skills-title">Matched Skills</div>
        ${matchedTags}
      </div>

      <div class="skills-section">
        <div class="skills-title">Missing Skills</div>
        ${missingTags}
      </div>
    `;
  } catch (error) {
    resultDiv.innerHTML = `<p style="color:#b3261e;">Error: ${error.message}</p>`;
  } finally {
    btn.disabled = false;
    btn.innerText = "Analyze Resume";
  }
}
