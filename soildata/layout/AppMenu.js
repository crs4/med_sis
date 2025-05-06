import AppSubMenu from './AppSubMenu';

const AppMenu = () => {
    const model = [
        {
            label: 'Home',
            icon: 'pi pi-home',
            items: [
                {
                    label: 'Catalogue',
                    icon: 'pi pi-fw pi-home',
                    to: '/'
                },
                {
                    label: 'Back Office',
                    icon: 'pi pi-fw pi-image',
                    to: '/soildata'
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
            label: 'Soil Profiles',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/profiles'
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/profiles/edit'
                },
                {
                    label: 'Publish',
                    icon: 'pi pi-fw pi-briefcase',
                    to: '/profiles/publish'
                },
                {
                    label: 'Backup',
                    icon: 'pi pi-fw pi-file',
                    to: '/profiles/backup'
                }
            ]
        },
        { separator: true },
        {
            label: 'Soil Samples',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/samples'
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/samples/edit'
                },
                {
                    label: 'Publish',
                    icon: 'pi pi-fw pi-briefcase',
                    to: '/samples/publish'
                },
                {
                    label: 'Backup',
                    icon: 'pi pi-fw pi-file',
                    to: '/samples/backup'
                }
            ]
        },
        { separator: true },
        {
            label: 'Soil Indicators',
            icon: 'pi pi-fw pi-image',
            items: [
                {
                    label: 'List',
                    icon: 'pi pi-fw pi-list',
                    to: '/indicators'
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/indicators/create'
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
                },
                {
                    label: 'New',
                    icon: 'pi pi-fw pi-plus',
                    to: '/photos/uploads'
                }
            ]
        }
    ];
    return <AppSubMenu model={model} />;
};

export default AppMenu;
