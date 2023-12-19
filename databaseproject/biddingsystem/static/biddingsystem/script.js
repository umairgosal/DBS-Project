function followUser(followBtn, event) {
    event.preventDefault();
    fetch("/profile/" + followBtn.dataset.followed + "/follow", {
        method: "POST",
        body: JSON.stringify({
            operation: "follow",
            follower: followBtn.dataset.follower,
            followed: followBtn.dataset.followed
        }),
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        const followersCount = document.getElementById('followers_count');
        followersCount.textContent = Number(followersCount.textContent) + 1;
        followBtn.textContent = "Unfollow";
        followBtn.setAttribute('onclick', 'unFollowUser(this, event)');
    })
    .catch(error => console.error('Error:', error));
}

function unFollowUser(unFollowBtn, event) {
    event.preventDefault();
    fetch("/profile/" + unFollowBtn.dataset.followed + "/follow", {
        method: "POST",
        body: JSON.stringify({
            operation: "unfollow",
            follower: unFollowBtn.dataset.follower,
            followed: unFollowBtn.dataset.followed
        }),
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        const followersCount = document.getElementById('followers_count');
        followersCount.textContent = Number(followersCount.textContent) - 1;
        unFollowBtn.textContent = "Follow";
        unFollowBtn.setAttribute('onclick', 'followUser(this, event)');
    })
    .catch(error => console.error('Error:', error));
}



function cancelPayment(cancelBtn, event) {
    event.preventDefault();
    paymentBox = document.getElementById('payment')
    paymentBox.style.display = 'none';
}

function pay(payBtn, event) {
    event.preventDefault();
    paymentBox = document.getElementById('payment')
    paymentBox.style.display = 'block';
}

function updateStripeAmount() {
    var amountInput = document.getElementById("amount").value;
    var stripeButton = document.getElementById("stripeButton");

    // Update the data-amount attribute with the user-input amount
    stripeButton.setAttribute("data-amount", "900");
}
