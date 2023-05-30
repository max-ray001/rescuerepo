import React from 'react';
import classNames from 'classnames';


const Title = ({ title, subtitle, className }) => {

  const classes = classNames('flex', 'flex-col', 'text-left', 'justify-center', 'font-sans', className);

  return (
    <div className={classes}>
      <h1 className="text-6xl font-medium">{title}</h1>
      <h2 className="text-2xl font-thin">{subtitle}</h2>
    </div>
  );
};

export default Title;