import AppSubMenu from './AppSubMenu';
import { useUser } from '../context/user';
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

const AppMenu = () => {
    const { userData } = useUser();
    const router = useRouter();
    const _model = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            to: process.env.NEXT_PUBLIC_CATALOGUE_BASE_URL
        },
        { separator: true },
        {
            label: 'XLS Uploads',
            icon: 'pi pi-download',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-list',
                    to: '/uploads'
                },
                {
                    label: 'New',
                    icon: 'pi pi-plus',
                    to: '/uploads/create'
                }
            ]
        },
        { separator: true },
        {
            label: 'Points Soil Data',
            icon: 'pi pi-map-marker',
            to: '/points'
        },
        { separator: true },
        {
            label: 'Publish',
            icon: 'pi pi-briefcase',
            to: '/publish'
        },
        { separator: true },
        {
            label: 'Taxonomies',
            icon: 'pi pi-book',
            to: '/taxonomy'
        },
        { separator: true },
        {
            label: 'Tools',
            icon: 'pi pi-briefcase',
            items: [
                {
                    label: 'Hydro PTF',
                    icon: 'pi pi-list',
                    to: '/hydroptf'
                },
                {
                    label: 'Area Soil Indicators',
                    icon: 'pi pi-wrench',
                    to: '/areasi'
                },
            ]
        }

    ];
    const [ model, setModel ] = useState(_model);
    
    return <AppSubMenu model={model} />;
};

export default AppMenu;
