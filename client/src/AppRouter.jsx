import React from 'react';
// import {Route, Routes, Router} from 'react-router-dom'
import {Switch } from 'react-router'
import {observer} from "mobx-react-lite";
import {  BrowserRouter as Router,  Routes,  Route} from "react-router-dom";

const AppRouter = observer(() => {
    // const {user} = useContext(Context)

    // console.log(user)
    return (
        // <Router>
        //     <Routes>
        //         <Route path="/about" element={<h2>About</h2>} />
        //         {/* <Route path="/contact" element={(<h2>Contacts</h2>)} />
        //         <Route path="/" element={(<h2>Nothing</h2>)} /> */}
        //     </Routes>
        // </Router>
        <div>
            
            <Router>
                <Routes>
                    <Route path="/" element={<h1>Салам</h1>}/>
                    <Route path="/students" element={<h1>Салам1</h1>}/>
                </Routes>
            </Router>
        </div>
        
    );
});

export default AppRouter;