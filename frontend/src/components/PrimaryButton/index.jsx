import React from 'react';
import classNames from 'classnames';


const Button = ({ text, onClick, className }) => {

    const classes = classNames('text-center', 'justify-center', 'hover:cursor-pointer', 'hover:bg-black', 'hover:text-gray-300', className);

    return (
        <div className={classes} onClick={onClick}>
            <h1>{text}</h1>
        </div>
    );
};

export default Button;