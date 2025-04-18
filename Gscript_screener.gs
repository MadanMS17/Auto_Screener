function convertResumeLinksToDirectDownload() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet4");  // your sheet name
  const data = sheet.getDataRange().getValues();
  
  for (let i = 1; i < data.length; i++) {
    const originalLink = data[i][9];  // J column (index 9)

    if (originalLink && originalLink.includes("drive.google.com/file/d/")) {
      // Extract the file ID
      const fileIdMatch = originalLink.match(/\/d\/(.*?)\//);
      if (fileIdMatch && fileIdMatch[1]) {
        const fileId = fileIdMatch[1];
        const directDownloadLink = `https://drive.google.com/uc?export=download&id=${fileId}`;

        // Write back to the same cell
        sheet.getRange(i + 1, 10).setValue(directDownloadLink);  // J column is index 10 in getRange (1-based)
        Logger.log(`✅ Converted link for row ${i + 1}`);
      } else {
        Logger.log(`⚠️ No valid file ID found in row ${i + 1}`);
      }
    }
  }
  
  SpreadsheetApp.flush();
  Logger.log("✅ All links processed.");
}


function processNewInternResumes() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet4");
  const data = sheet.getDataRange().getValues();

  const apiUrl = "https://auto-screener.onrender.com/screen_resume";

  for (let i = 1; i < data.length; i++) {
    const role = data[i][6];
    const resumeURL = data[i][9];
    const sentStatus = data[i][11];

    if (resumeURL && sentStatus !== "Sent") {
      try {
        const jobDescription = getJobDescriptionForRole(role);

        // Download PDF as blob
        const resumeBlob = UrlFetchApp.fetch(resumeURL).getBlob();

        // 🔍 Log content type here:
        const contentType = resumeBlob.getContentType();
        Logger.log("Row " + (i + 1) + " Content-Type: " + contentType);

        // Accept both PDF and octet-stream
        if (contentType !== "application/pdf" && contentType !== "application/octet-stream") {
          Logger.log("⚠️ Skipping row " + (i + 1) + " — invalid file type.");
          continue;
        }

        const resumeBase64 = Utilities.base64Encode(resumeBlob.getBytes());

        const payload = JSON.stringify({
          "job_description": jobDescription,
          "resume_base64": resumeBase64
        });

        const options = {
          "method": "post",
          "contentType": "application/json",
          "payload": payload,
          "muteHttpExceptions": true
        };

        const response = UrlFetchApp.fetch(apiUrl, options);
        const result = JSON.parse(response.getContentText());

        if (response.getResponseCode() === 200 && result.match_score !== undefined) {
          const score = result.match_score;
          sheet.getRange(i + 1, 11).setValue(score); // Column K — AI Resume Score

          // Score classification
          let classification = "";
          if (score >= 80) {
            classification = "🔥 Excellent";
          } else if (score >= 60) {
            classification = "✅ Good";
          } else if (score >= 40) {
            classification = "⚠️ Average";
          } else {
            classification = "❌ Needs Improvement";
          }

          // Set classification in Column L
          sheet.getRange(i + 1, 12).setValue(classification); // Column L
        }else {
          Logger.log("API Error for row " + (i + 1) + ": " + response.getContentText());
        }

      } catch (e) {
        Logger.log("Error processing row " + (i + 1) + ": " + e);
      }
    }
  }

  SpreadsheetApp.flush();
  Logger.log("✅ Resume screening process completed.");
}


function getJobDescriptionForRole(role) {
  const jobDescriptions = {
    "AIMLE": "Looking for AI/ML Engineers with experience in Python, data preprocessing, and model deployment.",
    "FSD": "We need Web Developers skilled in React, Node.js, MongoDB, and RESTful APIs.",
    "DATASCI": "Data Scientists required with experience in data analytics, Python, and machine learning models."
  };
  return jobDescriptions[role] || "Generic job description for this internship role.";
}
