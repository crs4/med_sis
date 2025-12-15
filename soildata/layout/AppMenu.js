import AppSubMenu from './AppSubMenu';
import { useUser } from '../context/user';
import React, { useEffect, useState } from 'react';

const AppMenu = () => {
    const user = useUser();
    const modelA = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            items: [
                {
                    label: 'Catalogue',
                    icon: 'pi pi-fw pi-home',
                    to: 'https://soils4med.crs4.it/'
                },
                {
                    label: 'Back Office',
                    icon: 'pi pi-fw pi-image',
                    to: '/'
                }
            ]
        },
        { separator: true },
        {
            label: 'Data Request',
            icon: 'pi pi-fw pi-briefcase',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/requests'
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/requests/create'
                },
                {
                    label: 'Elaborate',
                    icon: 'pi pi-fw pi-cog',
                    to: '/requests/elaborate'
                }
            ]
        },
        { separator: true },
        {
            label: 'XLS Uploads',
            icon: 'pi pi-fw pi-download',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/uploads'
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/uploads/create'
                }
            ]
        },
        { separator: true },
        {
            label: 'Points Soil Data',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/points'
                },
                {
                    label: 'Backup',
                    icon: 'pi pi-fw pi-file',
                    to: '/points/backup'
                }
            ]
        },
        { separator: true },
        {
            label: 'Photos',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/photos'
                }
            ]
        }
    ];
    const modelB = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            items: [
                {
                    label: 'Catalogue',
                    icon: 'pi pi-fw pi-home',
                    to: 'https://soil4med.crs4.it/'
                },
                {
                    label: 'Back Office',
                    icon: 'pi pi-fw pi-image',
                    to: '/'
                }
            ]
        },
        { separator: true },
        {
            label: 'Requests',
            icon: 'pi pi-fw pi-briefcase',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/requests'
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/requests/create'
                }
            ]
        }
    ];
    const [ model, setModel ] = useState(modelA);
    
    useEffect(() => {
        if ( !user.userData || 
             user.userData.forbidden1 === null ||  
             user.userData.forbidden1 ){
            setModel(modelB);
        }
        else setModel(modelA);
        
    }, [user]);

    return <AppSubMenu model={model} />;
};

export default AppMenu;
