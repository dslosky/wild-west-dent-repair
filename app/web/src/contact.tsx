import {KeyboardEvent, useState} from "react";
import ApiClient from "./api-client";

import "./home.css"
import "./contact.css"

function Contact() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [displayPhone, setDisplayPhone] = useState("");
  const [message, setMessage] = useState("");
  const [validPhone, setValidPhone ] = useState(true);
  const [validEmail, setValidEmail ] = useState(true);
  const [sentSuccess, setSentSuccess ] = useState(false);

  const apiClient = new ApiClient();

  const submit = () => {
    console.log(
      name, email, phone, message
    )

    let valid = true;
    if (!email.includes("@") || !email.includes(".") ) {
      setValidEmail(false);
      valid = false;
    }

    if (phone.length < 10) {
      setValidPhone(false);
      valid = false;
    }

    if (!valid) {return}

    setValidPhone(true);
    setValidEmail(true);
  
    apiClient.post("contact", {
      "name": name, "email": email, "phone": phone, "message": message
    });

    onSuccess();
  }

  const onSuccess = () => {
    setSentSuccess(true);
    setName("");
    setPhone("");
    setEmail("");
    setMessage("");
  }

  const changePhone = (event: KeyboardEvent) => {
    if (phone.length > 10) {
      return
    }

    let newPhone;
    if (event.key.toLowerCase().includes("backspace")) {
      newPhone = phone.slice(0, phone.length - 1);
    } else if ("0123456789".includes(event.key)) {
      newPhone = `${phone}${event.key}`
    } else {
      return
    }

    console.log(newPhone)
    setPhone(newPhone);
    setDisplayPhone("(".concat(newPhone.slice(0,3),") ",newPhone.slice(3,6), "-", newPhone.slice(6,10)))
  }

  return (
    <div className="contact-container">

        {sentSuccess ? 
        <div className="sentSuccess">
          <h1>Thank you for your message!</h1>
          <p>We will get back to you as soon as possible.</p>
        </div>:
        <div>
        <h1 className="title text-white font-bold drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
          Message Us
        </h1>
        <div className="messageForm">
          <form>
            <div>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Name" />
              <input 
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email" />
              <input
                value={displayPhone}
                onKeyDown={(event: KeyboardEvent) => changePhone(event)}
                placeholder="Phone" />
            </div>
            <textarea 
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Message"></textarea>
          </form>

          {!validEmail ? <p className="error">Invalid Email</p> : null}
          {!validPhone ? <p className="error">Invalid Phone</p> : null}
          <a onClick={submit} target="_blank" rel="noopener noreferrer" className="btn btn-blue">
            Send
          </a>
        </div>
      </div>
}
{/* 
        <a href="https://calendly.com/wild-west-dent-repair/consultation" target="_blank" rel="noopener noreferrer" className="btn btn-blue">
          Schedule a Consultation
        </a> */}
        
        <div className="welcome rounded overflow-hidden shadow-lg">

          <p>720.218.1614</p>

          <p>
            16039 W 4th Ave
            Golden, CO 80401
          </p>
        </div>
      </div>
  )
}

export default Contact
