function changing(){
    var account=document.getElementById("account").innerText;
    console.log(account);
    var d_one=document.getElementById('d_one');
    var d_two=document.getElementById('d_two');
    var d_three=document.getElementById('d_three');
    d_one.style.display="none";
    d_two.style.display="none";
    d_three.style.display="none";
    if (account=='supperadmin'){
        d_one.style.display="block";
        d_two.style.display="none";
        d_three.style.display="none";
    }
    if (account=='admin'){
        d_one.style.display="none";
        d_two.style.display="block";
        d_three.style.display="none";
    }
    if (account=='user'){
        d_one.style.display="none";
        d_two.style.display="none";
        d_three.style.display="block";
    }



}