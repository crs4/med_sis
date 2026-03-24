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
            to: '/'
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
                }
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
                {
                    label: 'Create',
                    icon: 'pi pi-plus',
                    to: '/taxonomy/create'
                }
            ]
        },
        { separator: true },
        {
            label: 'Data Creator',
            icon: 'pi pi-briefcase',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-list',
                    to: '/requests'
                },
                {
                    label: 'New',
                    icon: 'pi pi-plus',
                    to: '/requests/create'
                }
            ]
        },
        { separator: true },
        {
            label: 'Pedo Transfer Functions',
            icon: 'pi pi-calculator',
            items: [
                {
                    label: 'Training',
                    icon: 'pi pi-wrench',
                    to: '/ptf'
                },
                {
                    label: 'Executing',
                    icon: 'pi pi-play-circle',
                    to: '/ptf'
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
