const taskElement = document.getElementById("task");
const inputElement = document.getElementById("inputText");
const generateButton = document.getElementById("generateBtn");
const clearButton = document.getElementById("clearBtn");
const statusElement = document.getElementById("status");
const resultElement = document.getElementById("result");

const placeholders = {
    qa: "Ask a question, for example: What is the largest ocean?",
    explain: "Enter a concept, for example: Explain photosynthesis",
    quiz: "Enter a topic, for example: Pythagoras theorem",
    summarize: "Paste the text you want to summarize...",
    learn: "Enter a topic, for example: I want to learn SQL"
};

taskElement.addEventListener("change", () => {
    inputElement.placeholder = placeholders[taskElement.value] || placeholders.qa;
});

clearButton.addEventListener("click", () => {
    inputElement.value = "";
    resultElement.textContent = "Your AI-generated result will appear here.";
    statusElement.textContent = "";
});

generateButton.addEventListener("click", async () => {
    const task = taskElement.value;
    const text = inputElement.value.trim();

    if (!text) {
        statusElement.textContent = "Please enter a question or topic.";
        return;
    }

    statusElement.textContent = "Generating...";
    resultElement.textContent = "";
    generateButton.disabled = true;

    let endpoint = "";
    let body = {
        text: text
    };

    if (task === "qa") {
        endpoint = "/qa";
    } else if (task === "explain") {
        endpoint = "/explain";
    } else if (task === "quiz") {
        endpoint = "/quiz";
        body.count = 3;
    } else if (task === "summarize") {
        endpoint = "/summarize";
    } else if (task === "learn") {
        endpoint = "/learn/recommendations";
    }

    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Something went wrong."
            );
        }

        if (!data.success) {
            throw new Error("Request failed.");
        }

        if (task === "quiz") {
            renderQuiz(data.result);
        } else {
            resultElement.textContent = data.result;
        }

        statusElement.textContent = "Done!";
    } catch (error) {
        resultElement.textContent = "";
        statusElement.textContent = "Error: " + error.message;
    } finally {
        generateButton.disabled = false;
    }
});

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function renderQuiz(quizData) {
    if (!quizData || !Array.isArray(quizData.questions)) {
        resultElement.textContent = "Invalid quiz response.";
        return;
    }

    resultElement.innerHTML = "";

    quizData.questions.forEach((question, index) => {
        const questionBox = document.createElement("div");
        questionBox.className = "quiz-question";

        const title = document.createElement("h3");
        title.textContent = `${index + 1}. ${question.question}`;

        questionBox.appendChild(title);

        const options = document.createElement("div");
        options.className = "quiz-options";

        question.options.forEach((option) => {
            const optionElement = document.createElement("div");
            optionElement.className = "quiz-option";
            optionElement.textContent = option;

            options.appendChild(optionElement);
        });

        questionBox.appendChild(options);

        const answer = document.createElement("p");
        answer.innerHTML =
            `<strong>Answer:</strong> ${escapeHtml(question.correct_answer)}`;

        questionBox.appendChild(answer);

        const explanation = document.createElement("p");
        explanation.innerHTML =
            `<strong>Explanation:</strong> ${escapeHtml(question.explanation)}`;

        questionBox.appendChild(explanation);

        resultElement.appendChild(questionBox);
    });
}

inputElement.placeholder = placeholders.qa;