const checkIfUserExists = () => {
    const registrationForm = document.forms['registration-form']
    const emailFormElement = registrationForm['email-address']
    const email = emailFormElement.value
    axios.post('/validate-doctor', {
        email: email
    })
    .then((response) => {
        if(response.data.user_exists == "true") {
            emailFormElement.setCustomValidity('This user already exists, please login instead.')
            emailFormElement.reportValidity()
        }
    }, (error) => {
        console.log(error)
    })
}

const checkIfUserExistsWithEvent = (e) => {
    emailFormElement = e.target
    email = e.target.value
    console.log(email)
    axios.post('/validate-doctor', {
        email: email
    })
    .then((response) => {
        if(response.data.user_exists == "true") {
            emailFormElement.setCustomValidity('This user already exists, please login instead.')
            emailFormElement.reportValidity()
        }
    }, (error) => {
        console.log(error)
    })
}