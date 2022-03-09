import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import AppBlogForm from './AppBlogForm';
import AppBlogFormEdit from './AppBlogFormEdit';

import reportWebVitals from './reportWebVitals';

// ReactDOM.render(
//   <React.StrictMode>
//     <AppBlogForm />
//   </React.StrictMode>,
//   document.getElementById('root-blog-form')
// );

ReactDOM.render(
  <React.StrictMode>
    <AppBlogFormEdit />
  </React.StrictMode>,
  document.getElementById('root-blog-form-edit')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
