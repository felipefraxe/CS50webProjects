document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Send e-mail to database
  document.querySelector('#compose-form').onsubmit = compose;
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      const mail = document.createElement('div');
      const emailSender = document.createElement('div');
      const emailSubject = document.createElement('div');
      const emailTimestamp = document.createElement('div');

      if (email.read){
        mail.className = 'row card-header bg-secondary';
      } else {
        mail.className = 'row card-header bg-light';
      };

      emailSender.innerHTML = email.sender;
      emailSender.className = 'col-lg-3 col-md-3 col-sm-12';
      emailSubject.innerHTML = email.subject;
      emailSubject.className = 'col-lg-6 col-md-5 col-sm-12';
      emailTimestamp.innerHTML = email.timestamp;
      emailTimestamp.className = 'col-lg-3 col-md-3 col-sm-12';

      mail.append(emailSender, emailSubject, emailTimestamp);
      document.querySelector('#emails-view').append(mail);

      // Open Selected e-mail
      mail.addEventListener('click', () => open_email(email.id));
    })
  })
  .catch(error => console.log("Error", error));
}

function compose() {

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .catch(error => console.log('Error:', error));
  localStorage.clear();

  // Redurect user to sent section
  load_mailbox('sent');
  return false;
}

function open_email(email_id){
  
  // handle views
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#emails-view').style.display = 'none';
  let emailView = document.querySelector('#email-view');
  emailView.innerHTML = '';
  emailView.style.display = 'block';
  
  //Get clicked email content
  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
    const emailView = document.querySelector('#email-view');

    const emailSubject = document.createElement('div');
    
    const emailSender = document.createElement('div');
    const emailTimestamp = document.createElement('div');
    const senderTimestamp = document.createElement('div');
    
    const emailRecipient = document.createElement('div');
    
    const emailBody = document.createElement('div');

    // Enable archive/unarchive
    const archiveDiv = document.createElement('div');
    archiveDiv.className = 'col-lg-1 col-md-1 col-sm-1'
    const archiveButton = document.createElement('button');
    archiveButton.className = 'btn btn-sm btn-outline-primary';
    if (email.archived === false){
      archiveButton.innerHTML = 'Archive';
      archiveButton.addEventListener('click', () => archive_email(email_id));
    } else {
      archiveButton.innerHTML = 'Unarchive';
      archiveButton.addEventListener('click', () => unarchive_email(email_id));
    }
    archiveDiv.append(archiveButton);

    // Eneble reply
    const replyDiv = document.createElement('div');
    const replyButton = document.createElement('button');
    replyButton.className = 'btn btn-sm btn-outline-primary';
    replyButton.innerHTML = 'Relpy';
    replyButton.addEventListener('click', () => reply(email.id));
    replyDiv.append(replyButton);

    const buttons = document.createElement('div');
    buttons.className = 'row';
    buttons.append(replyDiv, archiveDiv);

    //construction of email display
    emailSubject.innerHTML = `<h4>${email.subject}</h4>`;
    
    emailSender.innerHTML = `<strong>${email.sender}</strong>`;
    emailSender.className = 'col-lg-8 col-md-5 col-sm-12';

    emailTimestamp.innerHTML = `<small>${email.timestamp}</small>`;
    emailTimestamp.className = 'col-lg-3 col-md-3 col-sm-12';
    
    senderTimestamp.className = 'row';
    senderTimestamp.append(emailSender, emailTimestamp);

    emailRecipient.innerHTML = `<small>for: ${email.recipients}</small>`;
    
    emailBody.innerHTML = `<br><p>${email.body}</p>`;

    emailView.append(emailSubject, senderTimestamp, emailRecipient, emailBody, buttons);
  })
  .catch(error => console.log('Error: ', error));

  //Mark as read
  read_email(email_id);
  return false;
}

function read_email(email_id){
  
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true
    })
  })
  .catch(error => console.log('Error: ', error));
  return false;
}

function archive_email(email_id){
  
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: true
    })
  })
  .catch(error => console.log('Error: ', error));

  localStorage.clear();
  load_mailbox('inbox');
  return false;
}

function unarchive_email(email_id){
  
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: false
    })
  })
  .catch(error => console.log('Error: ', error));

  localStorage.clear();
  load_mailbox('inbox');
  return false;
}

function reply(email_id){

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {

    compose_email();
    document.querySelector('#compose-recipients').value = `${email.sender}`;
    if (email.subject.slice(0,3) === 'Re:'){
      document.querySelector('#compose-subject').value = `${email.subject}`;
    } else {
      document.querySelector('#compose-subject').value = `Re: ${email.subject}`;
    }
    document.querySelector('#compose-body').value = `On ${email.timestamp}, ${email.sender} wrote: ${email.body}`;
  })
  .catch(error => console.log('Error: ', error));
  return false;
}