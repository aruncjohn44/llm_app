document
  .getElementById("rag-form")
  .addEventListener("submit", async function(event) {
    event.preventDefault();

    const prompt = document.getElementById("prompt").value;
    const temperature = document.getElementById("temperature").value;
    const model = document.getElementById("model").value;

    const responseBox = document.getElementById("response-box");
    responseBox.innerHTML = "Generating response...";

    try {
      const response = await fetch("/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          prompt: prompt,
          temperature: temperature,
          model: model
        })
      });

      const result = await response.json();
      responseBox.innerHTML = `<pre>${result.response}</pre>`;
    } catch (error) {
      responseBox.innerHTML = `<p class="text-danger">Error: ${error.message}</p>`;
    }
  });
