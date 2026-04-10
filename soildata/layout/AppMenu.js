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
            icon: 'pi pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-list',
                    to: '/points'
                },
            ]
        },
        { separator: true },
        {
            label: 'Taxonomies',
            icon: 'pi pi-book',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-list',
                    to: '/taxonomy'
                },
            ]
        },
        { separator: true },
        {
            label: 'Elaboration',
            icon: 'pi pi-briefcase',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-list',
                    to: '/request'
                },
            ]
        },
        { separator: true },
        {
            label: 'PTF',
            icon: 'pi pi-calculator',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-list',
                    to: '/ptf'
                },
                {
                    label: 'New',
                    icon: 'pi pi-wrench',
                    to: '/ptf/create'
                }
            ]
        },
        { separator: true },
        {
            label: 'Help',
            icon: 'pi pi-question-circle',
            items: [
                {
                    label: 'manuals',
                    icon: 'pi pi-list',
                    to: '/help'
                },
                {
                    label: 'videos',
                    icon: 'pi pi-list',
                    to: '/help/videos'
                }
            ]
        }

    ];
    const [ model, setModel ] = useState(_model);
    
    return <AppSubMenu model={model} />;
};

export default AppMenu;
