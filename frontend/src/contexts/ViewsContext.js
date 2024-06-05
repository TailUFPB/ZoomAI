import React from 'react';

export const ViewsContext = React.createContext();

export function ViewsProvider({ children }) {
    const [viewIndex, setViewIndex] = React.useState(0);

    return (
        <ViewsContext.Provider value={{ viewIndex, setViewIndex }}>
            {children}
        </ViewsContext.Provider>
    );
};
