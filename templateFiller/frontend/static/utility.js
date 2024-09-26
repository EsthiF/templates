class Utility {
    constructor() {
        this.assetCounter = 1; 
    }

      // Sum fields
      sumFields(fieldIds) {
        let total = 0;
        fieldIds.forEach(id => {
            const fieldValue = document.getElementById(id)?.value || 0;
            total += parseFloat(fieldValue);
        });
        return total;
    }

    // Search function for filtering forms
    searchForms() {
        console.log("Search function is running");

        let input = document.getElementById('search-input').value.toLowerCase();
        let formCards = document.getElementsByClassName('card');

        for (let i = 0; i < formCards.length; i++) {
            let formName = formCards[i].getElementsByTagName('a')[0].getAttribute('data-form-name').toLowerCase();

            if (formName.includes(input)) {
                formCards[i].style.display = "";  
            } else {
                formCards[i].style.display = "none";  
            }
        }
    }

  

    // Multiply two fields
    multiplyFields(field_1, field_2) {
        return parseFloat(field_1 || 0) * parseFloat(field_2 || 0);
    }

    // Divide two fields
    divideFields(numerator, denominator) {
        if (denominator == 0) {
            return "Division by zero is not allowed";
        }
        return parseFloat(numerator || 0) / parseFloat(denominator || 1);
    }

    // Method to dynamically add new asset fields to the form
    addAsset() {
        const assetSection = document.getElementById('asset-details-section');
        const newAssetHTML = `
            <div class="asset-item">
                <div class="form-group">
                    <label for="asset_name_${this.assetCounter}"> מה שם הנכס?</label>
                    <input type="text" id="asset_name_${this.assetCounter}" name="assets[${this.assetCounter}][name]" required>
                </div>
                <div class="form-group">
                    <label for="asset_type_${this.assetCounter}"> מה סוג הנכס?</label>
                    <input type="text" id="asset_type_${this.assetCounter}" name="assets[${this.assetCounter}][type]" required>
                </div>
                <div class="form-group">
                    <label for="asset_value_${this.assetCounter}"> מה הערך של הנכס?</label>
                    <input type="number" id="asset_value_${this.assetCounter}" name="assets[${this.assetCounter}][value]" required>
                </div>
            </div>
        `;
        assetSection.insertAdjacentHTML('beforeend', newAssetHTML);
        this.assetCounter++;
    }
    validateFormSteps(formSteps) {
        let isValid = true;

        formSteps.forEach(step => {
            const requiredFields = step.querySelectorAll("input[required], select[required]");
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add("error"); // Highlight the empty field
                    field.focus(); // Focus on the first empty field
                } else {
                    field.classList.remove("error"); // Remove error class if the field is filled
                }
            });
        });

        if (!isValid) {
            alert("Please fill all required fields before submitting the form.");
        }

        return isValid;
    }

    // Validate the current step
    validateCurrentStep(currentStep, formSteps) {
        const currentFields = formSteps[currentStep].querySelectorAll("input[required], select[required]");
        let isValid = true;

        currentFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add("error"); // Highlight the empty field
                field.focus(); // Focus on the first empty field
            } else {
                field.classList.remove("error"); // Remove error class if the field is filled
            }
        });

        return isValid;
    }
}

const utility = new Utility();



function calculateSums() {
    const sum_1 = utility.sumFields(['m_amount', 'm_amount_1']);
    const sum_2 = utility.sumFields(['l_amount', 'l_amount_1']);
    const sum_3 = utility.sumFields(['sum_2', 'value']);


    document.getElementById('sum_1').value = sum_1;
    document.getElementById('sum_2').value = sum_2;
    document.getElementById('sum_3').value = sum_3;

    console.log(`Calculated sum_1: ${sum_1}`);
    console.log(`Calculated sum_2: ${sum_2}`);
    console.log(`Calculated sum_2: ${sum_3}`);

    return true;  
}
