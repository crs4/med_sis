import React, { useState, useEffect, useContext } from "react";

export const userContext = React.createContext();

const initialState = {
  access_token : null,
  sub: null,
  name: null,
  given_name: null,
  family_name: null,
  email: null,
  preferred_username: null,
  groups: [],
  forbidden: null,
};


export const UserProvider = (props) => {
  const [userData, setUserData] =  useState(initialState);

  useEffect(() => {
    const getUserProfile = async () => {
      try {
        let res = await fetch('/api/o/v4/userinfo');
        if ( res && res.status === 200 ) {
          let data = await res.json();
          if ( !data.groups || ( data.groups.indexOf('admin') !== -1 &&  data.groups.indexOf('datamanager') !== -1 ) )
            data.forbidden = true;
          else data.forbidden = false;
          setUserData(data);
        }
        else {
          let state = {
            access_token : null,
            sub: null,
            name: null,
            given_name: null,
            family_name: null,
            email: null,
            preferred_username: null,
            groups: [],
            forbidden: true,
          };
          setUserData(state);
        }  
      } catch (error) {
        setUserData(initialState);
      }
    }
    getUserProfile();
  }, []);


  const exposed = {
    userData,
  };

  return <userContext.Provider value={exposed}>{props.children}</userContext.Provider>;
};

export const useUser = () => useContext(userContext);


