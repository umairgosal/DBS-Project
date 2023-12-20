async function followUser (followBtn, event) {
    event.preventDefault();
    await fetch("follow", {
        method: "POST",
        body: JSON.stringify({
            operation: "follow",
            followed: followBtn.dataset.followed,
            follower: followBtn.dataset.follower
        })}).then(response => response.json()).then(result => {
            console.log(result)
            followersCount = document.getElementById('followers_count')
            followersCount.textContent = Number(followersCount.textContent) + 1
            followBtn.textContent = "Unfollow"
            followBtn.setAttribute('onclick', 'unFollowUser(this, event)')
        })
}   

async function unFollowUser(unFollowBtn, event) {
    event.preventDefault();
    await fetch("follow", {
        method: "POST",
        body: JSON.stringify({
            operation: "unfollow",
            followed: unFollowBtn.dataset.followed,
            follower: unFollowBtn.dataset.follower
        })}).then(response => response.json()).then(result => {
            console.log(result)
            followersCount = document.getElementById('followers_count')
            followersCount.textContent = Number(followersCount.textContent) - 1
            unFollowBtn.textContent = "Follow"
            unFollowBtn.setAttribute('onclick', 'followUser(this, event)')
        })
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