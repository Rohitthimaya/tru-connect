// Updating Year for footer
// 3.2.1 G requirement Met 
// 3.2.6 A requirement Met
document.getElementById("year").textContent = new Date().getFullYear();


// Validating Feedback Form 3.2.6 B & C requirement Met
function validateForm() {
    // Making sure name is not empty.
    let name = document.forms["feedbackForm"]["name"].value;
    if (name == "") {
      alert("Name must be filled out");
      document.forms["feedbackForm"]["name"].value = name;
    }

    // Make sure its email
    let email = document.forms["feedbackForm"]["email"].value;
    if(email == ""){
        alert("Email Must Be Filled OUT");
        document.forms["feedbackForm"]["email"].value = email;
    }else if(email.indexOf("@") == -1){
        alert("Please Enter Valid Email")
        document.forms["feedbackForm"]["email"].value = email;
    }

    // Make sure message is given
    let msg = document.forms["feedbackForm"]["message"].value;
    if(msg == ""){
        alert("Message Cannot Be Blank...");
    }
  }
