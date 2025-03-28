function predict_foodexp() {
    const salary=document.getElementById("salary").value
    console.log(salary)
    document.getElementById("foodexp").innerText = 
        "predicted food exp " + ((salary*0.4815)+147.4)
}