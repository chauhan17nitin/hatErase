// notification
const notification = document.querySelector('.notification');

const showNotification = (message) => {
    notification.textContent = message;
    notification.classList.add('active');
    setTimeout(() => {
        notification.classList.remove('active');
        notification.textContent = ''
    }, 4000);
};


export class AppComponent  {

    public isVisible: boolean = false;
  
    showAlert() : void {
      if (this.isVisible) { // if the alert is visible return
        return;
      } 
      this.isVisible = true;
      setTimeout(()=> this.isVisible = false,2500); // hide the alert after 2.5s
    }
  
  }