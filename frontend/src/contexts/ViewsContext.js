import React from 'react';

export const ViewsContext = React.createContext();

export function ViewsProvider({ children }) {
    const [viewIndex, setViewIndex] = React.useState(0);

    React.useEffect(() => {
        console.log('View index changed:', viewIndex);
    }
    , [viewIndex]);

    return (
        <ViewsContext.Provider value={{ viewIndex, setViewIndex }}>
            {children}
        </ViewsContext.Provider>
    );
};
