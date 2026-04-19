let display = document.getElementById("display");
let panel = document.getElementById("panel");

// Allowed characters only
function isValidInput(char) {
    return /[0-9+\-*/().]/.test(char);
}

// Add value (button click)
function add(value) {
    display.value += value;
}

// Prevent typing letters
display.addEventListener("input", function () {
    let value = display.value;
    let filtered = "";

    for (let i = 0; i < value.length; i++) {
        if (isValidInput(value[i])) {
            filtered += value[i];
        }
    }

    display.value = filtered;
});

// Clear
function clearScreen() {
    display.value = "";
}

// Backspace
function backspace() {
    display.value = display.value.slice(0, -1);
}

// Toggle panel
function togglePanel() {
    panel.style.display = (panel.style.display === "block") ? "none" : "block";
}

// Calculate
function calculate() {
    fetch("/calculate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            expression: display.value
        })
    })
    .then(res => res.json())
    .then(data => {
        display.value = data.result;
    });
}