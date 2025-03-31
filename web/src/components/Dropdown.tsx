import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/20/solid'
import React, { useCallback, useState } from 'react'

export function Dropdown(props: { title: string; children: React.ReactNode }) {
    const { title, children } = props
    const [isOpen, setIsOpen] = useState(false)
    const onClick = useCallback(() => {
        setIsOpen(!isOpen)
    }, [isOpen])
    const header = (
        <div className="flex px-4 py-2 items-center justify-between">
            <span className="text-md font-medium">{title}</span>
            {isOpen ? (
                <ChevronUpIcon className="w-8 h-8 text-gray-500" />
            ) : (
                <ChevronDownIcon className="w-8 h-8 text-gray-500" />
            )}
        </div>
    )
    const style: React.CSSProperties = {
        transition: 'height 0.3s ease-in-out',
    }
    const line = (
        <div
            className="h-px bg-gray-300"
            style={{
                opacity: isOpen ? 1 : 0,
            }}
        />
    )
    const childrenContainer = isOpen ? <div className="flex px-4 py-2">{children}</div> : undefined
    return (
        <div
            className="flex flex-col border border-gray-300 rounded-md"
            style={style}
            onClick={onClick}
        >
            {header}
            {line}
            {childrenContainer}
        </div>
    )
}
