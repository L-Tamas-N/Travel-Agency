const payNowButton = document.getElementById('pay-now-button');
    
payNowButton.addEventListener('click', async () => {
    const reservationId = {{ reservation.id }};

    const response = await fetch('/process_payment/', {
        method: 'POST',  
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            reservation_id: reservationId,  
        }),
    });

    const data = await response.json();
    if (data.sessionId) {
        const stripe = Stripe('your-publishable-key-here');
        stripe.redirectToCheckout({ sessionId: data.sessionId });
    } else {
        alert('Payment failed: ' + data.error);
    }
});