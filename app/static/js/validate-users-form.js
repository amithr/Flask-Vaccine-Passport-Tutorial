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

const checkIfPasswordIsValid = () => {
    const loginForm = document.forms['login-form']
    const passwordFormElement = loginForm['password']
    const emailFormElement = loginForm['password']
    const password = passwordFormElement.value
    const email = emailFormElement.value
    axios.post('/validate-password', {
        email: email,
        password: password
    })
    .then((response) => {
        if(response.data.user_exists == "false") {
            passwordFormElement.setCustomValidity("Password doesn't match user or user doesn't exist.")
            emailFormElement.reportValidity()
            return false
        }
        return true
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