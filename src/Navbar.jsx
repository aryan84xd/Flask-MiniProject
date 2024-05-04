import React from "react";
// import logo from "https://www.shutterstock.com/image-vector/dog-paw-icon-260nw-439718731.jpg"
function Navbar()
{
    return <nav className="Navbar">
    <img src="https://www.shutterstock.com/image-vector/dog-paw-icon-260nw-439718731.jpg"alt=""></img>
    <ul>
        <li>Home</li>
        <li>About us</li>
        <li>Donate</li>
        <li>Adopt</li>
        <li>Events</li>
        <li>Contact US</li>

    </ul>
    <div className="LogButn">
        LOGIN
    </div>
    
    </nav>
}

export default Navbar;