import AppSubMenu from './AppSubMenu';
import { useUser } from '../context/user';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

const AppMenu = () => {
    const { userData } = useUser();
    const router = useRouter();
    const modelA = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            items: [
                {
                    label: 'Catalogue',
                    icon: 'pi pi-fw pi-home',
                    to: process.env.NEXT_PUBLIC_CATALOGUE_BASE_URL
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
                    label: 'Catalogue',
                    icon: 'pi pi-fw pi-list',
                    to: '/points/catalogue'
                }
            ]
        },
        { separator: true },
        {
            label: 'Taxonomies',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/taxonomy'
                },
            ]
        },
        { separator: true },
        {
            label: 'Data Creator',
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
        },
        { separator: true },
        {
            label: 'Pedo Transfer Functions',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/ptf'
                },
                {
                    label: 'Elaborate',
                    icon: 'pi pi-fw pi-plus',
                    to: '/ptf/elaborate'
                }
            ]
        },
        { separator: true },
        {
            label: 'Help',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'manuals',
                    icon: 'pi pi-fw pi-list',
                    to: '/help'
                },
                {
                    label: 'videos',
                    icon: 'pi pi-fw pi-list',
                    to: '/help/videos'
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
                    to: process.env.NEXT_PUBLIC_CATALOGUE_BASE_URL
                }
            ]
        }
    ]
    const [ model, setModel ] = useState(modelB);
        
    useEffect(() => {
        if ( userData && userData.forbidden !== null && !userData.forbidden )
            setModel(modelA);    
    }, [userData]);
    
    return <AppSubMenu model={model} />;
};

export default AppMenu;
