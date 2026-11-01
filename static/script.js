const analyseButton = document.getElementById("analyseButton");

const statementA = document.getElementById("statementA");
const statementB = document.getElementById("statementB");

const statusText = document.getElementById("status");
const resultSection = document.getElementById("resultSection");


analyseButton.addEventListener("click", async () => {

    const textA = statementA.value.trim();
    const textB = statementB.value.trim();

    if (!textA || !textB) {
        statusText.textContent = "Please enter both statements.";
        return;
    }

    analyseButton.disabled = true;
    analyseButton.textContent = "Analysing...";
    statusText.textContent = "Gemini is analysing your statements...";
    resultSection.classList.add("hidden");

    try {

        const response = await fetch("/analyse", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                statement_a: textA,
                statement_b: textB
            })
        });

        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || "Analysis failed.");
        }

        document.getElementById("classification").textContent =
            result.classification.replaceAll("_", " ").toUpperCase();

        document.getElementById("explanation").textContent =
            result.explanation;

        document.getElementById("confidence").textContent =
            result.confidence.toUpperCase();

        const evidenceList = document.getElementById("evidence");
        evidenceList.replaceChildren();

        result.evidence.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            evidenceList.appendChild(li);
        });

        const explanationsList =
            document.getElementById("possibleExplanations");

        explanationsList.replaceChildren();

        result.possible_explanations.forEach(item => {
            const li = document.createElement("li");
            li.textContent = item;
            explanationsList.appendChild(li);
        });

        resultSection.classList.remove("hidden");
        statusText.textContent = "Analysis completed!";

    } catch (error) {

        statusText.textContent = error.message;

    } finally {

        analyseButton.disabled = false;
        analyseButton.textContent = "Analyse Statements";

    }

});