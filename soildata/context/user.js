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
  forbidden: true,
};


export const UserProvider = (props) => {
  const [userData, setUserData] =  useState(initialState);

  useEffect(() => {
    const getUserProfile = async () => {
      try {
        let res = await fetch('/api/o/v4/userinfo');
        console.log (res);
        if ( res && res.status == 200 ) {
          let userdata = await res.json();
          if ( !userdata.groups || ( userdata.groups.indexOf('admin') === -1 &&  userdata.groups.indexOf('datamanager') === -1 ) )
            userdata.forbidden = true;
          else userdata.forbidden = false;
          setUserData({
            ...userdata,
          });
        }
        else
          setUserData(initialState); 
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


