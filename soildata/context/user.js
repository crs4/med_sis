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
};


export const UserProvider = (props) => {
  const [userData, setUserData] =  useState(initialState);

  useEffect(() => {
    const getUserProfile = async () => {
      try {
        let res = await fetch('/api/o/v4/userinfo');
        if ( res && res.status == 200 ) {
          setUserData({
            ...res.data,
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
    setUser: (user) => {
      setUserData({ ...userData, ...user });
    },
    isDataManager: () => {
      if ( !groups || ( groups.indexOf('admin') === -1 &&  groups.indexOf('datamanager') === -1 ) )
        return false;
      return true;
    },
    resetData: () => {
      setUserData({ ...initialState });
    },
  };

  return <userContext.Provider value={exposed}>{props.children}</userContext.Provider>;
};

export const useUser = () => useContext(userContext);


