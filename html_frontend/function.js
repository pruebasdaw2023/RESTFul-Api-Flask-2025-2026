// alert("Hola mundo")

const API = 'http://localhost:5000/products'

const listar_productos = async() => {

    const res = await fetch(API);
    const data = await res.json()
    console.log(data)

}

window.addEventListener("load", function(){
    listar_productos();
})




